import datetime

from bluzelle.sdk.bluzelle import Bluzelle
import uuid as u
from bluzelle.codec.crud.tx_pb2 import MsgCreate
from bluzelle.codec.crud.lease_pb2 import Lease
from bluzelle.codec.crud.query_pb2 import QueryReadRequest

uuid = str(u.uuid4())

sdk = Bluzelle(
        mnemonic="space dilemma domain payment snap crouch arrange"
        " fantasy draft shaft fitness rain habit dynamic tip "
        "faith mushroom please power kick impulse logic wet cricket",
        host="https://client.sentry.testnet.private.bluzelle.com",
        port=26657,
        max_gas=100000000,
        gas_price=0.002,
    )
print("\n\n\n\n Create a key value has been started ********************* \n\n\n\n")
sdk.db.tx.Create(
        MsgCreate(
            creator=sdk.wallet.address,
            uuid=uuid,
            key="myKey",
            value="myValue".encode("utf-8"),
            lease=Lease(hours=1),
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
print(f"Created key: myKey, value: myValue in {datetime.datetime.now()}")
print("\n\n\n\n Create a key value has been ended ********************* \n\n\n\n")

print("\n\n\n\n Read a key value has been started ********************* \n\n\n\n")
response = sdk.db.q.Read(
        QueryReadRequest(
            uuid=uuid,
            key="myKey",
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
print(response)
print("\n\n\n\n End a key value has been ended ********************* \n\n\n\n")