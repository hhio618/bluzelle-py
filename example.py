import datetime
import time

from bluzelle.codec.cosmos.bank.v1beta1.query_pb2 import QueryBalanceRequest
from bluzelle.codec.crud.lease_pb2 import Lease
from bluzelle.codec.crud.query_pb2 import QueryReadRequest, QueryGetLeaseRequest, QueryKeyValuesRequest, QuerySearchRequest, QueryGetNShortestLeasesRequest
from bluzelle.codec.crud.tx_pb2 import MsgCreate, MsgUpdate, MsgRenewLeasesAll
from bluzelle.sdk.bluzelle import Bluzelle

uuid = str((datetime.datetime.now() - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000.0)


def populate_uuid(sdk):
    sdk.db.withTransactions([
        MsgCreate(
            creator=sdk.db.address,
            uuid=uuid,
            key='firstKey',
            value='firstValue'.encode('utf-8'),
            metadata=[],
            lease=Lease(hours=1),
        ),
        MsgCreate(
            creator=sdk.db.address,
            uuid=uuid,
            key='secondKey',
            value='firstValue'.encode('utf-8'),
            metadata=[],
            lease=Lease(hours=1),
        ),
        MsgCreate(
            creator=sdk.db.address,
            uuid=uuid,
            key='thirdKey',
            value='firstValue'.encode('utf-8'),
            metadata=[],
            lease=Lease(hours=1),
        )
    ],
        memo='optionalMemo')


def diff_cost_with_different_lease(sdk):
    response = sdk.bank.Q.balance(
        None,
        QueryBalanceRequest(
            address=sdk.db.address,
            denom='ubnt',
        ),
    )
    firstCost = int(response.balance.amount)
    sdk.db.tx.create_(
        None,
        MsgCreate(
            creator=sdk.db.address,
            uuid=uuid,
            key='someKeyA',
            value='someValue'.encode('utf-8'),
            lease=Lease(hours=1),
        ),
    )
    response = sdk.bank.Q.balance(
        None,
        QueryBalanceRequest(
            address=sdk.db.address,
            denom='ubnt',
        ),
    )
    firstCost -= int(response.balance.amount)
    # creating another key 
    response = sdk.bank.Q.balance(
        None,
        QueryBalanceRequest(
            address=sdk.db.address,
            denom='ubnt',
        ),
    )
    secondCost = int(response.balance.amount)
    sdk.db.tx.create_(
        None,
        MsgCreate(
            creator=sdk.db.address,
            uuid=uuid,
            key='someKeyB',
            value='someValue'.encode('utf-8'),
            lease=Lease(days=1),
        ),
    )
    response = sdk.bank.Q.balance(
        None,
        QueryBalanceRequest(
            address=sdk.db.address,
            denom='ubnt',
        ),
    )
    secondCost -= int(response.balance.amount)

    return secondCost - firstCost


def diff_cost_equal_message_size(sdk):
    response = sdk.bank.Q.balance(
        None,
        QueryBalanceRequest(
            address=sdk.db.address,
            denom='ubnt',
        ),
    )
    firstCost = int(response.balance.amount)
    sdk.db.tx.create_(
        None,
        MsgCreate(
            creator=sdk.db.address,
            uuid=uuid,
            key='someKeyA',
            value='someValue'.encode('utf-8'),
            lease=Lease(hours=1),
        ),
    )
    response = sdk.bank.Q.balance(
        None,
        QueryBalanceRequest(
            address=sdk.db.address,
            denom='ubnt',
        ),
    )
    firstCost -= int(response.balance.amount)
    # creating another key 
    response = sdk.bank.Q.balance(
        None,
        QueryBalanceRequest(
            address=sdk.db.address,
            denom='ubnt',
        ),
    )
    secondCost = int(response.balance.amount)
    sdk.db.tx.create_(
        None,
        MsgCreate(
            creator=sdk.db.address,
            uuid=uuid,
            key='someKeyB',
            value='someValue'.encode('utf-8'),
            lease=Lease(hours=1),
        ),
    )
    response = sdk.bank.Q.balance(
        None,
        QueryBalanceRequest(
            address=sdk.db.address,
            denom='ubnt',
        ),
    )
    secondCost -= int(response.balance.amount)

    return secondCost - firstCost


if __name__ == '__main__':
    sdk = Bluzelle(
        mnemonic="space dilemma domain payment snap "
                 "crouch arrange fantasy draft shaft fitness rain habit "
                 "dynamic tip faith mushroom please power kick impulse logic wet cricket",
        host='https://client.sentry.testnet.private.bluzelle.com',
        port=26657,
        max_gas=100000000,
        gas_price=0.002,
    )

    print(f'Created key: myKey, value: myValue in {datetime.datetime.now()}')
    sdk.db.tx.Create(
        None,
        MsgCreate(
            creator=sdk.wallet.address,
            uuid=uuid,
            key='myKey',
            value='myValue'.encode('utf-8'),
            lease=Lease(hours=1),
        )
    )
    response = sdk.db.q.Read(
        None,
        QueryReadRequest(
            uuid=uuid,
            key='myKey',
        )
    )
    print(f'Read key: myKey, value: {response.value} in {datetime.datetime.now()}')
    sdk.db.tx.update(
        None,
        MsgUpdate(
            creator=sdk.wallet.address,
            uuid=uuid,
            key='myKey',
            value='updatedValue'.encode('utf-8'),
            lease=Lease(minutes=1),
        )
    )

    response = sdk.db.q.Read(
        None,
        QueryReadRequest(
            uuid=uuid,
            key='myKey',
        )
    )
    print(f'Update key: myKey, value: {response.value} in {datetime.datetime.now()}')
    response = sdk.db.q.get_lease(
        None,
        QueryGetLeaseRequest(
            uuid=uuid,
            key='myKey',
        )
    )
    print(f"remaining lease time {response.seconds}")
    populate_uuid(sdk)
    print('Creating 3 new key-value pairs')

    # fetch the inserted values 
    response = sdk.db.Q.keyValues(
        None,
        QueryKeyValuesRequest(uuid=uuid),
    )
    print(f'Reading all values in {datetime.datetime.now()}, {response.keyValues}')

    cost_difference = diff_cost_with_different_lease(sdk)
    print(f'Total cost difference for 2 create with different lease {cost_difference}')

    cost_difference = diff_cost_equal_message_size(sdk)
    print(f'Total cost difference for 2 equal size creates is {cost_difference}')

    response = sdk.db.q.Search(
        None,
        QuerySearchRequest(
            uuid=uuid,
            searchString='s',
        )
    )
    print(f'Key-values matching the search string "s": {response.keyValues} ')
    response = sdk.db.Q.getNShortestLeases(
        None,
        QueryGetNShortestLeasesRequest(
            uuid=uuid,
            num=5,
        )
    )

    print(f"Getting 5 shortest lease {response}")
    sdk.db.tx.RenewLeasesAll(
        None,
        MsgRenewLeasesAll(
            creator=sdk.wallet.address,
            uuid=uuid,
            lease=Lease(seconds=10),
        )
    )
    print(f"Update leases to 10 seconds for all key-values")
    response = sdk.db.q.GetNShortestLeases(
        None,
        QueryGetNShortestLeasesRequest(
            uuid=uuid,
            num=6,
        )
    )
    print(f"Getting 6 shortest lease {response}")
    time.sleep(10)
    response = sdk.db.q.KeyValues(
        None,
        QueryKeyValuesRequest(uuid=uuid)
    )
    print(f"Querying all key-values in {datetime.datetime.now()}")
