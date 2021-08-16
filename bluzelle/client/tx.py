import time
from typing import List

from google.protobuf.message import Message

from bluzelle.client.query import QueryClient
from bluzelle.codec.cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from bluzelle.codec.cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest, QueryAccountResponse
from bluzelle.codec.cosmos.auth.v1beta1.query_pb2_grpc import QueryStub
from bluzelle.codec.cosmos.base.v1beta1.coin_pb2 import Coin
from bluzelle.codec.cosmos.tx.signing.v1beta1.signing_pb2 import SIGN_MODE_DIRECT
from bluzelle.codec.cosmos.tx.v1beta1.tx_pb2 import Fee
from bluzelle.cosmos import Transaction
from bluzelle.cosmos._sign_mode_handler import DirectSignModeHandler
from bluzelle.cosmos._wallet import Wallet
from bluzelle.tendermint import Tendermint34Client
from .rpc import Callable, RpcChannel


class TxCallable(Callable):
    """TxCallable will be used to receiving grpc calls from the user and sending them back to the
    :term:`TransactionClient` using the :term:`sender` callback function.
    """

    def __init__(
        self,
        tendermint34Client: Tendermint34Client,
        method: str,
        request_serializer,
        response_deserializer,
        sender,
    ):
        super().__init__(tendermint34Client, method, request_serializer, response_deserializer)
        # Callback function to take care of broadcasting a signed tx.
        self.sender = sender

    def _blocking(self, request, timeout, metadata, credentials, wait_for_ready, compression):
        self.sender(request)


class TransactionClient(RpcChannel):
    """TransactionClient acts as a bridge between custom protobuf Message.

    type transaction requests and Tendermint34Client.broadcast_tx_sync.
    """

    def __init__(
        self,
        tendermint34Client: Tendermint34Client,
        query_client: QueryClient,
        wallet: Wallet,
        max_gas: int,
        gas_price: float,
    ):
        """Creating a new TransactionClient.

        Args:
          tendermint34Client: A Tendermint34Client instance to make calls against bluzelle tendermint rpc.
          query_client: A QueryClient instance needed for getting
              account data prior to the sending transactions.
          wallet: Required for signing raw transactions.
          max_gas: Maximum gas could be used by in transactions.
          gas_price: Together with :term:`max_gas` will be used to calculating transaction fees.
        """
        self.wallet = wallet
        self.max_gas = max_gas
        self.gas_price = gas_price
        self.query_client = query_client
        super().__init__(tendermint34Client)

    def unary_unary(self, method, request_serializer, response_deserializer):
        return TxCallable(
            self.tendermint34Client,
            method,
            request_serializer,
            response_deserializer,
            self.send,
        )

    def send(self, message: Message) -> bytes:
        return self.with_transactions([message])

    def with_transactions(self, messages: List[Message], memo: str = None) -> bytes:
        """Sending multiple grpc Messages at once, and wait for it to be
        included in a block."""
        signed_tx = self.prepair_transaction(messages, memo)

        # Sending transaction on-chain and receiving the tx hash.
        tx_hash = self.submit_transaction(signed_tx)

        # Block until the transaction is included in a block successfully or failed.
        self.wait_transaction_done(tx_hash)

    def prepair_transaction(self, messages: List[Message], memo: str):
        """Creating a offline signed transaction using input messages and
        wallet data."""

        # Account data need to create a raw transaction.
        account = self.get_account()

        # Getting chain id using tendermint cliend.
        chain_id = self.get_chain_id()

        # Calculating the transaction fee.
        fee = Fee(
            gas_limit=self.max_gas,
            amount=[Coin(denom="ubnt", amount=str(int(self.max_gas * self.gas_price)))],
        )

        # Creating the raw transaction.
        tx = Transaction(
            account=account,
            messages=messages,
            sign_mode=SIGN_MODE_DIRECT,
            privkey=self.wallet.private_key,
            fee=fee,
            memo=memo,
            chain_id=chain_id,
        ).create()

        # Signing the transaction offline.
        signed_tx = tx.sign(
            sign_mode_handler=DirectSignModeHandler(),
        )

        print("#####################################")
        print(signed_tx)
        print("#####################################")
        return signed_tx

    def submit_transaction(self, signed_tx: bytes) -> str:
        """Broadcasting the signed transaction using the tendermint client.

        Args:
          signed_tx: the signed transaction bytes data.

        Returns:
          The transaction hash (will be used to query the transaction data later).
        """
        result = self.tendermint34Client.broadcast_tx_sync(signed_tx)
        return result["hash"]

    def wait_transaction_done(self, hash: str):
        """Block until the transaction is included in a block successfully or
        failed.

        Args:
          hash: The input transaction hash.

        Raises:
          ValueError: will be raised if the transaction has been failed.
        """
        # Query the transaction using its hash.
        timeout = time.time() + 60 * 10  # 10 minutes from now
        time.sleep(10)
        while time.time() < timeout:
            response = self.tendermint34Client.tx_search(query=f"tx.hash='{hash}'")
            if int(response["total_count"]) > 0:
                tx = response["txs"][0]["tx_result"]
                # if tx['code'] != 0 or len(tx['events']) == 0:
                if tx["code"] != 0:
                    code = tx["code"]
                    log = tx["log"]
                    code_space = tx["codespace"]
                    raise ValueError(
                        f"call failed with code {code} (log: {log}, codespace: {code_space}))"
                    )
                return
            # Waiting 10 seconds before making another rpc call.
            time.sleep(10)

    def get_account(self) -> BaseAccount:
        """Getting account information by making a Account rpc call using the
        tendermint client.

        Raises:
          ValueError: A ValueError will be raised if the resulting account is None or it's address
        differ from the :term:`wallet` address
        """
        queryApi = QueryStub(self.query_client)
        request = QueryAccountRequest(address=self.wallet.address)
        response: QueryAccountResponse = queryApi.Account(
            request,
            timeout=3000,
            metadata=None,
            credentials=None,
            wait_for_ready=True,
            compression=False,
        )
        if response.account is None:
            raise ValueError("Resulting account from abci_query should not be None!")
        account = BaseAccount.FromString(response.account.value)
        account = account
        if account.address != self.wallet.address:
            raise ValueError(
                "Resulting account from abci_query should be equal to the wallet address!"
            )
        return account

    def get_chain_id(self) -> str:
        node_info = self.tendermint34Client.status()
        return node_info["node_info"]["network"]
