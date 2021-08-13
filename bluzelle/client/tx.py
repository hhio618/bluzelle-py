
from bluzelle.codec.cosmos.tx.signing.v1beta1.signing_pb2 import SignMode, SIGN_MODE_DIRECT
from bluzelle.client import query
from bluzelle.client.query import QueryClient
from bluzelle.client.rpc import RpcChannel
import time
import json
from base64 import b64decode
from typing import List
from google.protobuf import json_format
from bluzelle.tendermint import Tendermint34Client
from google.protobuf.message import Message
from bluzelle.codec.cosmos.tx.v1beta1.service_pb2 import BroadcastTxResponse
from bluzelle.codec.cosmos.tx.v1beta1.tx_pb2 import Tx
from bluzelle.codec.cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from bluzelle.codec.cosmos.auth.v1beta1.query_pb2_grpc import QueryStub
from bluzelle.codec.cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest, QueryAccountResponse
from bluzelle.cosmos._wallet import Wallet
from bluzelle.cosmos import Transaction
from bluzelle.cosmos._sign_mode_handler import DirectSignModeHandler
from .rpc import Callable, RpcChannel



class TxCallable(Callable):
    def __init__(self, tendermint34Client: Tendermint34Client, method: str, request_serializer, response_deserializer, sender):
        super().__init__(tendermint34Client, method, request_serializer, response_deserializer)
        self.sender = sender
    def __call__(self, request, timeout, metadata, credentials, wait_for_ready, compression):
        self.sender(request)
        
    

class TransactionClient(RpcChannel):
    def __init__(self, tendermint34Client: Tendermint34Client, query_client: QueryClient ,wallet: Wallet, max_gas: int, gas_price: float):
        self.wallet = wallet
        self.max_gas = max_gas
        self.gas_price = gas_price
        self.query_client = query_client
        super().__init__(tendermint34Client)
    
    def unary_unary(self, method, request_serializer, response_deserializer):
        return TxCallable(self.tendermint34Client, method, request_serializer, response_deserializer, self.send)

    def send(self, req: Message) -> bytes:
        return self.with_transactions([req])

    def with_transactions(self, reqs: List[Message]) -> bytes:
        signed_tx = self.prepair_transaction(reqs)
        tx = self.submit_transaction(signed_tx)
        self.wait_transaction_done(tx)

    def prepair_transaction(self, reqs: List[Message]):
        account = self.get_account(self.wallet.address)
        chain_id = self.get_chain_id()
        tx = Transaction(
            privkey=self.wallet.private_key,
            account_num=account.account_number,
            sequence=account.sequence,
            fee=self.max_gas* self.gas_price,
            gas=self.max_gas,
            memo="",
            chain_id=chain_id,
        )
        signed_tx = tx.sign(account, SIGN_MODE_DIRECT, sign_mode_handler=DirectSignModeHandler(), messages=reqs)
        return signed_tx

    
    def submit_transaction(self, signed_tx: bytes):
        result = self.tendermint34Client.broadcast_tx_sync(signed_tx)
        return result

    def wait_transaction_done(self, tx: BroadcastTxResponse):
        print("tx: ", tx)
        print("tx(type): ", type(tx))
        # Query the transaction using its hash.
        # timeout = time.time() + 60*10   # 10 minutes from now
        # while time.time() < timeout:
        #     response = self.tendermint34Client.tx_search("tx.hash={tx.Hash}")
        #     if response.totalCount > 0:
        #         tx = response.txs[0].tx_result
        #         if tx.code != 0 or tx.events.is_empty:
        #             raise ValueError("call failed with code {tx.code} (log: {tx.log}, codespace: {tx.code_space}))")
        #     time.sleep(20)

    def get_account(self, address) -> BaseAccount:
        queryApi = QueryStub(self.query_client)
        request = QueryAccountRequest(address=address)
        response: QueryAccountResponse =  queryApi.Account(request,
                timeout=3000,
                metadata=None,
                credentials=None,
                wait_for_ready=True, 
                compression=False)
        if response.account is None:
            return None
        account = BaseAccount.FromString(response.account.value)
        print("************* Got account: ",account)
        account = account
        if account.address != address:
            return None
        return account
    
    def get_chain_id(self) -> BaseAccount:
       node_info = self.tendermint34Client.status()

       return node_info['node_info']['network']
        