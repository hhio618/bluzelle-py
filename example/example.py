import datetime
import time
import uuid as u
import asyncio
from bluzelle.codec.cosmos.bank.v1beta1.query_pb2 import QueryBalanceRequest
from bluzelle.codec.crud.lease_pb2 import Lease
from bluzelle.codec.crud.query_pb2 import (
    QueryGetLeaseRequest,
    QueryGetNShortestLeasesRequest,
    QueryKeyValuesRequest,
    QueryReadRequest,
    QuerySearchRequest,
)
from bluzelle.codec.crud.tx_pb2 import MsgCreate, MsgRenewLeasesAll, MsgUpdate
from bluzelle.sdk.bluzelle import Bluzelle

uuid = str(u.uuid4())


def populate_uuid(sdk):
    sdk.db.with_transactions(
        [
            MsgCreate(
                creator=sdk.wallet.address,
                uuid=uuid,
                key="firstKey",
                value="firstValue".encode("utf-8"),
                lease=Lease(hours=1),
            ),
            MsgCreate(
                creator=sdk.wallet.address,
                uuid=uuid,
                key="secondKey",
                value="firstValue".encode("utf-8"),
                lease=Lease(hours=1),
            ),
            MsgCreate(
                creator=sdk.wallet.address,
                uuid=uuid,
                key="thirdKey",
                value="firstValue".encode("utf-8"),
                lease=Lease(hours=1),
            ),
        ],
        memo="optionalMemo",
    )


async def diff_cost_with_different_lease(sdk):
    response_1 = await sdk.bank.q.Balance(
        QueryBalanceRequest(
            address=sdk.wallet.address,
            denom="ubnt",
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    first_cost = int(response_1.balance.amount)
    await sdk.db.tx.Create(
        MsgCreate(
            creator=sdk.wallet.address,
            uuid=uuid,
            key="someKeyA",
            value="someValue".encode("utf-8"),
            lease=Lease(hours=1),
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    response_2 = await sdk.bank.q.Balance(
        QueryBalanceRequest(
            address=sdk.wallet.address,
            denom="ubnt",
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    first_cost -= int(response_2.balance.amount)
    # creating another key
    response_3 = await sdk.bank.q.Balance(
        QueryBalanceRequest(
            address=sdk.wallet.address,
            denom="ubnt",
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    second_cost = int(response_3.balance.amount)
    await sdk.db.tx.Create(
        MsgCreate(
            creator=sdk.wallet.address,
            uuid=uuid,
            key="someKeyB",
            value="someValue".encode("utf-8"),
            lease=Lease(days=1),
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    response_4 = await sdk.bank.q.Balance(
        QueryBalanceRequest(
            address=sdk.wallet.address,
            denom="ubnt",
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    second_cost -= int(response_4.balance.amount)

    return second_cost - first_cost


async def diff_cost_equal_message_size(sdk):
    response_1 = await sdk.bank.q.Balance(
        QueryBalanceRequest(
            address=sdk.wallet.address,
            denom="ubnt",
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    first_cost = int(response_1.balance.amount)
    await sdk.db.tx.Create(
        MsgCreate(
            creator=sdk.wallet.address,
            uuid=uuid,
            key="someKeyA",
            value="someValue".encode("utf-8"),
            lease=Lease(hours=1),
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    response_2 = await sdk.bank.q.Balance(
        QueryBalanceRequest(
            address=sdk.wallet.address,
            denom="ubnt",
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    first_cost -= int(response_2.balance.amount)
    # creating another key
    response_3 = await sdk.bank.q.Balance(
        QueryBalanceRequest(
            address=sdk.wallet.address,
            denom="ubnt",
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    second_cost = int(response_3.balance.amount)
    await sdk.db.tx.Create(
        MsgCreate(
            creator=sdk.wallet.address,
            uuid=uuid,
            key="someKeyB",
            value="someValue".encode("utf-8"),
            lease=Lease(hours=1),
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    response_4 = await sdk.bank.q.Balance(
        QueryBalanceRequest(
            address=sdk.wallet.address,
            denom="ubnt",
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    second_cost -= int(response_4.balance.amount)

    return second_cost - first_cost


async def main(sdk):
    await sdk.db.tx.Create(
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
    response = await sdk.db.q.Read(
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
    print(f"Read key: myKey, value: {response.value} in {datetime.datetime.now()}")

    await sdk.db.tx.Update(
        MsgUpdate(
            creator=sdk.wallet.address,
            uuid=uuid,
            key="myKey",
            value="updatedValue".encode("utf-8"),
            lease=Lease(minutes=1),
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )

    response = await sdk.db.q.Read(
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
    print(f"Update key: myKey, value: {response.value} in {datetime.datetime.now()}")
    response = await sdk.db.q.GetLease(
        QueryGetLeaseRequest(
            uuid=uuid,
            key="myKey",
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    print(f"remaining lease time {response.seconds}")
    populate_uuid(sdk)
    print("Creating 3 new key-value pairs")

    # fetch the inserted values
    response = await sdk.db.q.KeyValues(
        QueryKeyValuesRequest(uuid=uuid),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    print(f"Reading all values in {datetime.datetime.now()}, {response.keyValues}")

    cost_difference = await diff_cost_with_different_lease(sdk)
    print(f"Trueotal cost difference for 2 create with different lease {cost_difference}")
    #
    cost_difference = await diff_cost_equal_message_size(sdk)
    print(f"Total cost difference for 2 equal size creates is {cost_difference}")

    response = await sdk.db.q.Search(
        QuerySearchRequest(
            uuid=uuid,
            searchString="s",
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    print(f'Key-values matching the search string "s": {response.keyValues} ')
    response = await sdk.db.q.GetNShortestLeases(
        QueryGetNShortestLeasesRequest(
            uuid=uuid,
            num=5,
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )

    print(f"Getting 5 shortest lease {response}")
    await sdk.db.tx.RenewLeasesAll(
        MsgRenewLeasesAll(
            creator=sdk.wallet.address,
            uuid=uuid,
            lease=Lease(seconds=10),
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    print("Update leases to 10 seconds for all key-values")
    response = await sdk.db.q.GetNShortestLeases(
        QueryGetNShortestLeasesRequest(
            uuid=uuid,
            num=6,
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    print(f"Getting 6 shortest lease {response}")
    time.sleep(10)
    response = await sdk.db.q.KeyValues(
        QueryKeyValuesRequest(uuid=uuid),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    print(f"Querying all key-values in {datetime.datetime.now()}")


if __name__ == "__main__":
    sdk = Bluzelle(
        mnemonic="space dilemma domain payment snap crouch arrange"
        " fantasy draft shaft fitness rain habit dynamic tip "
        "faith mushroom please power kick impulse logic wet cricket",
        host="https://client.sentry.testnet.private.bluzelle.com",
        port=26657,
        max_gas=100000000,
        gas_price=0.002,
    )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(sdk))
    loop.close()
