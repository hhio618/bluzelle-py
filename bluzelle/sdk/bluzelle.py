from typing import Any
from mnemonic import Mnemonic
from bluzelle.tendermint import Tendermint34Client
from cosmospy import generate_wallet, BIP32DerivationError, seed_to_privkey, privkey_to_pubkey, pubkey_to_address
from bluzelle.wallet import Wallet
from bluzelle.client import QueryClient, TransactionClient
from bluzelle.codec.crud.query_pb2_grpc import QueryStub
from bluzelle.codec.crud.tx_pb2_grpc import MsgStub
from bluzelle.codec.cosmos.bank.v1beta1.query_pb2_grpc import QueryStub as BankQueryStub
from bluzelle.codec.cosmos.bank.v1beta1.tx_pb2_grpc import MsgStub as BankMsgStub
from typing import TypeVar, Generic, List

BLUEZELLE_DERIVATION_PATH = "m/44'/118'/0'/0/0"
BLUEZELLE_BECH32_HRP = "bluzelle"

Q = TypeVar('Q')
TX = TypeVar('TX')
class BluzelleSDK(Generic[Q,TX]):
      q: Q
      tx: TX

class Bluzelle:
      db: BluzelleSDK
      bank: BluzelleSDK
      wallet: Wallet
      
      def __init__(self, mnemonic: str, host: str, port: int, max_gas: int, gas_price: float):
            self.wallet = Wallet()
            if mnemonic is None:
                  w = generate_wallet(hrp=BLUEZELLE_BECH32_HRP)
                  self.wallet.seed = w["seed"]
                  self.wallet.private_key = w["private_key"]
                  self.wallet.address = w["address"]
                  self.wallet.public_key = w["public_key"]
                  self.wallet.derivation_path = w["derivation_path"]
            else:
                  try:
                        path = "m/44'/118'/0'/0/0"
                        privkey = seed_to_privkey(mnemonic, path=path)
                        pubkey = privkey_to_pubkey(privkey)
                        addr = pubkey_to_address(pubkey, hrp=BLUEZELLE_BECH32_HRP)
                        self.wallet.derivation_path = path
                        self.wallet.seed = mnemonic
                        self.wallet.private_key = privkey
                        self.wallet.address = addr
                        self.wallet.public_key = pubkey
                  except BIP32DerivationError:
                        print("No valid private key in this derivation path!")
            # Clients
            self.tendermint34Client = Tendermint34Client(host, port)
            self.query_client = QueryClient(self.tendermint34Client) 
            self.tx_client = TransactionClient(self.tendermint34Client, self.query_client, self.wallet, max_gas, gas_price) 
            
            # Defining db SDK
            self.db = BluzelleSDK[QueryStub, MsgStub]()
            self.db.q = QueryStub(self.query_client)
            self.db.tx = MsgStub(self.tx_client)

            # Defining bank SDK
            self.bank = BluzelleSDK[BankQueryStub, BankMsgStub]()
            self.bank.q = BankQueryStub(self.query_client)
            self.bank.tx = BankMsgStub(self.tx_client)