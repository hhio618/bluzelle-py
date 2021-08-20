from typing import Generic, TypeVar

from bluzelle.client import QueryClient, TransactionClient
from bluzelle.codec.cosmos.bank.v1beta1.query_pb2_grpc import QueryStub as BankQueryStub
from bluzelle.codec.cosmos.bank.v1beta1.tx_pb2_grpc import MsgStub as BankMsgStub
from bluzelle.codec.crud.query_pb2_grpc import QueryStub
from bluzelle.codec.crud.tx_pb2_grpc import MsgStub
from bluzelle.cosmos import (
    PATH,
    BIP32DerivationError,
    generate_wallet,
    privkey_to_pubkey,
    pubkey_to_address,
    seed_to_privkey,
)

# bluzelle.cosmos package contains a modified version of the original cosmospy library
# (https://github.com/hukkin/cosmospy) to handle customized bluzelle transactions.
from bluzelle.cosmos.typing import Wallet
from bluzelle.tendermint import Tendermint34Client

Q = TypeVar("Q")
TX = TypeVar("TX")


class BluzelleSDK(Generic[Q, TX]):
    q: Q
    tx: TX


class Bluzelle:
    db: BluzelleSDK
    bank: BluzelleSDK
    wallet: Wallet
    """Bluzelle is the main class for accessing Bluzelle SDKs."""

    def __init__(self, mnemonic: str, host: str, port: int, max_gas: int, gas_price: float):
        """Crating new Bluzelle instance.

        Args:
            mnemonic: Optional user provided mnemonic for deriving the wallet.
            host: Tendermint host for making rpc calls.
            port: Tendermint rpc port.
            max_gas: Maximum allowed gas limit for sending transaction.
            gas_price: Gas price in ubnt.

        Returns:
            New instance of the Bluzelle API.
        """
        self.wallet = Wallet()
        if mnemonic is None:
            # Generating a random wallet.
            w = generate_wallet()
            self.wallet.seed = w["seed"]
            self.wallet.private_key = w["private_key"]
            self.wallet.address = w["address"]
            self.wallet.public_key = w["public_key"]
            self.wallet.derivation_path = w["derivation_path"]
        else:
            try:
                privkey = seed_to_privkey(mnemonic)
                pubkey = privkey_to_pubkey(privkey)
                addr = pubkey_to_address(pubkey)
                self.wallet.derivation_path = PATH
                self.wallet.seed = mnemonic
                self.wallet.private_key = privkey
                self.wallet.address = addr
                self.wallet.public_key = pubkey
            except BIP32DerivationError:
                print("No valid private key in this derivation path!")

        # Creating a Tendermint RPC client.
        self.tendermint34Client = self.create_tendermint_client(host=host, port=port)

        # Creating grpc Query clients.
        self.query_client = QueryClient(self.tendermint34Client)
        self.tx_client = TransactionClient(
            self.tendermint34Client, self.query_client, self.wallet, max_gas, gas_price
        )

        # Defining the db SDK.
        self.db = BluzelleSDK[QueryStub, MsgStub]()
        self.db.q = QueryStub(self.query_client)
        self.db.with_transactions = self.tx_client.with_transactions
        self.db.tx = MsgStub(self.tx_client)

        # Defining the bank SDK
        self.bank = BluzelleSDK[BankQueryStub, BankMsgStub]()
        self.bank.q = BankQueryStub(self.query_client)
        self.bank.with_transactions = self.tx_client.with_transactions
        self.bank.tx = BankMsgStub(self.tx_client)

    def create_tendermint_client(self, host, port):
        """Tendermint is the transport for making grpc calls, sending new tx,
        ..."""
        return Tendermint34Client(host, port)
