from bluzelle.sdk.bluzelle import Bluzelle
from bluzelle.codec.crud.lease_pb2 import Lease
from bluzelle.codec.crud.tx_pb2 import MsgCreate, MsgUpdate, MsgRenewLeasesAll
from bluzelle.codec.crud.query_pb2 import (QueryBalanceRequest, QueryReadRequest, QueryGetLeaseRequest,
                                           QueryKeyValuesRequest, QuerySearchRequest, QueryGetNShortestLeasesRequest)
import datetime
import time 

uuid = str((datetime.datetime.now() - datetime.datetime.utcfromtimestamp(0)).total_seconds() * 1000.0)

def populateUuid(sdk):
    sdk.db.withTransactions([
      MsgCreate(
        creator= sdk.db.address,
        uuid= uuid,
        key= 'firstKey',
        value= 'firstValue'.encode('utf-8'),
        metadata= [],
        lease= Lease(hours= 1),
      ),
      MsgCreate(
        creator= sdk.db.address,
        uuid= uuid,
        key= 'secondKey',
        value= 'firstValue'.encode('utf-8'),
        metadata= [],
        lease= Lease(hours= 1),
      ),
      MsgCreate(
        creator= sdk.db.address,
        uuid= uuid,
        key= 'thirdKey',
        value= 'firstValue'.encode('utf-8'),
        metadata= [],
        lease= Lease(hours= 1),
      )
    ],
    memo= 'optionalMemo')


def diffCostForLeaseChange(sdk):
    response = sdk.bank.Q.balance(
        None,
        QueryBalanceRequest(
          address= sdk.db.address,
          denom= 'ubnt',
        ),
      )
    firstCost = int(response.balance.amount)
    sdk.db.tx.create_(
          None,
          MsgCreate(
            creator= sdk.db.address,
            uuid= uuid,
            key= 'someKeyA',
            value= 'someValue'.encode('utf-8'),
            lease= Lease(hours= 1),
          ),
        )
    response = sdk.bank.Q.balance(
          None,
          QueryBalanceRequest(
            address= sdk.db.address,
            denom= 'ubnt',
          ),
        )
    firstCost -= int(response.balance.amount)
    # creating another key 
    response = sdk.bank.Q.balance(
        None,
        QueryBalanceRequest(
          address= sdk.db.address,
          denom= 'ubnt',
        ),
      )
    secondCost = int(response.balance.amount)
    sdk.db.tx.create_(
          None,
          MsgCreate(
            creator= sdk.db.address,
            uuid= uuid,
            key= 'someKeyB',
            value= 'someValue'.encode('utf-8'),
            lease= Lease(days= 1),
          ),
        )
    response = sdk.bank.Q.balance(
          None,
          QueryBalanceRequest(
            address= sdk.db.address,
            denom= 'ubnt',
          ),
        )
    secondCost -= int(response.balance.amount)

    return secondCost - firstCost




def diffCostForEqualSizeCreates(sdk):
    response = sdk.bank.Q.balance(
        None,
        QueryBalanceRequest(
          address= sdk.db.address,
          denom= 'ubnt',
        ),
      )
    firstCost = int(response.balance.amount)
    sdk.db.tx.create_(
          None,
          MsgCreate(
            creator= sdk.db.address,
            uuid= uuid,
            key= 'someKeyA',
            value= 'someValue'.encode('utf-8'),
            lease= Lease(hours= 1),
          ),
        )
    response = sdk.bank.Q.balance(
          None,
          QueryBalanceRequest(
            address= sdk.db.address,
            denom= 'ubnt',
          ),
        )
    firstCost -= int(response.balance.amount)
    # creating another key 
    response = sdk.bank.Q.balance(
        None,
        QueryBalanceRequest(
          address= sdk.db.address,
          denom= 'ubnt',
        ),
      )
    secondCost = int(response.balance.amount)
    sdk.db.tx.create_(
          None,
          MsgCreate(
            creator= sdk.db.address,
            uuid= uuid,
            key= 'someKeyB',
            value= 'someValue'.encode('utf-8'),
            lease= Lease(hours= 1),
          ),
        )
    response = sdk.bank.Q.balance(
          None,
          QueryBalanceRequest(
            address= sdk.db.address,
            denom= 'ubnt',
          ),
        )
    secondCost -= int(response.balance.amount)

    return secondCost - firstCost


if __name__ == '__main__':
    sdk = Bluzelle(
         mnemonic=
        'switch wing oven chat cargo smile hello broken fluid puzzle endorse family divorce boat viable mutual film steel future casino economy lens december roast',
        host= 'wss://client.sentry.testnet.private.bluzelle.com',
        port= 26657,
        maxGas= 100000000,
        gasPrice= 0.002,
    )
    sdk.db.tx.create_(
        None,
        MsgCreate(
          creator= sdk.db.address,
          uuid= uuid,
          key= 'myKey',
          value= 'myValue'.encode('utf-8'),
          lease= Lease(hours= 1),
        )
      )
    print(f'Created key: myKey, value: myValue in {datetime.datetime.now()}')
    response = sdk.db.Q.read(
          None,
          QueryReadRequest(
            uuid= uuid,
            key= 'myKey',
          )
    )
    print(f'Read key: myKey, value: {response.value} in {datetime.datetime.now()}')
    sdk.db.tx.update(
        None,
        MsgUpdate(
          creator= sdk.db.address,
          uuid= uuid,
          key= 'myKey',
          value= 'updatedValue'.encode('utf-8'),
          lease= Lease(minutes= 1),
        )
      )

    response = sdk.db.Q.read(
          None,
          QueryReadRequest(
            uuid= uuid,
            key= 'myKey',
          )
    )
    print(f'Update key: myKey, value: {response.value} in {datetime.datetime.now()}')
    response = sdk.db.Q.getLease(
        None,
        QueryGetLeaseRequest(
          uuid= uuid,
          key= 'myKey',
        )
      )
    print(f"remaining lease time {response.seconds}")
    populateUuid(sdk)
    print('Creating 3 new key-value pairs')

    # fetch the inserted values 
    response = sdk.db.Q.keyValues(
        None,
        QueryKeyValuesRequest(uuid= uuid),
      )
    print(f'Reading all values in {datetime.datetime.now()}, {response.keyValues}')

    cost_difference = diffCostForLeaseChange(sdk)
    print(f'Total cost difference for 2 create with different lease {cost_difference}')

    cost_difference = diffCostForEqualSizeCreates(sdk)
    print(f'Total cost difference for 2 equal size creates is {cost_difference}')

    response = sdk.db.Q.search(
        None,
        QuerySearchRequest(
          uuid= uuid,
          searchString= 's',
        )
      )
    print(f'Key-values matching the search string "s": {response.keyValues} ')
    response = sdk.db.Q.getNShortestLeases(
        None,
        QueryGetNShortestLeasesRequest(
          uuid= uuid,
          num= 5,
        )
      )

    print(f"Getting 5 shortest lease {response}")
    sdk.db.tx.renewLeasesAll(
        None,
        MsgRenewLeasesAll(
          creator= sdk.db.address,
          uuid= uuid,
          lease= Lease(seconds= 10),
        )
      )
    print(f"Update leases to 10 seconds for all key-values")
    response = sdk.db.Q.getNShortestLeases(
        None,
        QueryGetNShortestLeasesRequest(
          uuid= uuid,
          num= 6,
        )
      )
    print(f"Getting 6 shortest lease {response}")
    time.sleep(10)
    response = sdk.db.Q.keyValues(
        None,
        QueryKeyValuesRequest(uuid= uuid)
      )
    print(f"Querying all key-values in {datetime.datetime.now()}")

    
    

    






    
    