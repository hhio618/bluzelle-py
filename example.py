from grpc import CallCredentials
from uuid import uuid4
from bluzelle.sdk.bluzelle import Bluzelle
from bluzelle.codec.cosmos.bank.v1beta1.query_pb2 import QueryBalanceRequest
from bluzelle.codec.crud.tx_pb2 import MsgCreate
from bluzelle.codec.crud.lease_pb2 import Lease



if __name__ == '__main__':
    sdk = Bluzelle(
        mnemonic="space dilemma domain payment snap crouch arrange fantasy draft shaft fitness rain habit dynamic tip faith mushroom please power kick impulse logic wet cricket",
        host='https://client.sentry.testnet.private.bluzelle.com',
        port=26657, 
        max_gas=100000000,
        gas_price=0.002,
    )

    sdk.db.tx.Create(
        MsgCreate(
            creator="bluzelle1qlme4k6gdrw25vues9kcz3nm6w8c38ml82kz5k",
            uuid="uuid",
            key='kir',
            value="kos".encode("utf-8"),
            lease=Lease(hours=1),
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True, 
        compression=False,
      )
    