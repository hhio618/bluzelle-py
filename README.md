# Bluzelle python API

![Build workflow](https://github.com/hhio618/bluzelle-py/actions/workflows/main.yml/badge.svg)
[![codecov](https://codecov.io/gh/hhio618/bluzelle-py/branch/main/graph/badge.svg?token=KPGB41FS6X)](https://codecov.io/gh/hhio618/bluzelle-py)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub license](https://img.shields.io/github/license/hhio618/bluzelle-py)](https://github.com/hhio618/bluzelle-py/blob/master/LICENSE)

<a href="https://bluzelle.com/"><img src='https://raw.githubusercontent.com/bluzelle/api/master/source/images/Bluzelle%20-%20Logo%20-%20Big%20-%20Colour.png' alt="Bluzelle" style="width: 100%"/></a>

**Bluzelle-py** is a Python library that can be used to access the Bluzelle database service.

# Setup

The Python Library is not yet published on any package manager, To install and use follow the below instructions:

```sh
$ # build the library
$ pip install "poetry==1.1.7"
$ poetry config virtualenvs.create false
$ poetry install --no-interaction --no-ansi
$ pip install .
```

# Publishing

There is a Github action that deploys new releases (using new tags) to the PyPI packages. (required to obtain a PYPI_TOKEN from the https://pypi.org website and adding it to the Github repository secrets.)

# Quick Start

To connect your instance to the Bluzelle testnet, you can:

1. mint an account by visiting **https://client.sentry.testnet.private.bluzelle.com:1317/mint**, which will provide a mnemonic and an address. This may take a while.

1. check your balance at **https://client.sentry.testnet.private.bluzelle.com:1317/bank/balances/{address}**. If your account balance is 0, mint another account until a positive ubnt balance shows

1. configure your sdk instance with the following options:

```python
from bluzelle.sdk.bluzelle import Bluzelle

sdk = Bluzelle(
    mnemonic="space dilemma domain payment snap crouch arrange"
    " fantasy draft shaft fitness rain habit dynamic tip "
    "faith mushroom please power kick impulse logic wet cricket",
    host="https://client.sentry.testnet.private.bluzelle.com",
    port=26657,
    max_gas=100000000,
    gas_price=0.002,
)
```

Note: if the specified gasPrice and/or maxGas is too low, any transactions may be rejected by a validator (e.g. a transaction requires more gas than maxGas specified, or the gasPrice is too low to cover validator fees). The default suggestion for these fields above will suffice.

Note: if you want to run examples in library folder, place the codes inside a file in the root directory

### Websockets vs. HTTPS

- The sdk supports both https and wss connections to the Bluzelle testnet
- For **https** pass the url **https://client.sentry.testnet.private.bluzelle.com:26657** to the bluzelle constructor.
- For **websockets** pass the url **wss://client.sentry.testnet.private.bluzelle.com:26657**.

Note: for both version first create a sdk instance then use a asyncio loop to run the program.
For more details on this see example/example.py.

# Usage

## sdk-hierarchy

_After configuring your sdk, you will have access to various modules and their corresponding methods._

- **Hierarchal format:**

```
sdk.[module].[q or tx or field].[Method](**kwargs)
```

- **Available Modules**: db, nft, staking, bank, distribution
- **Available Fields**: url, address, withTransactions(fn)

## Queries

_Each method takes a single parameter as an object (i.e. request), and returns an object (i.e. response). To see the request and response types, see the curium/proto/\[module\] for queries and transactions._

- Crud module query:

```python
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
print(reponse)
```

\*Note: response is a Uint8Array representing the byte-encoded value that had been queried. To get the string-representation of the value, use new TextDecoder().decode(resp.value)

- Bank module query:

```python
response = await sdk.bank.q.Balance(
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
print(response)
```

## Transactions

_The sdk can also send transactions to the chain. Each module has a tx method to send various transaction messages._

- Crud module tx:

```python
await sdk.db.tx.Create(
    MsgCreate(
        creator=sample_creator,
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
```

\*Note: the sdk is signing and sending the transaction, so the signer address must match the creator of the transaction. Otherwise, an error will be thrown

\*\*Note: see bluzelle.codec.crud.lease_pb2 to see the Lease interface

<!--
- Bank module tx:
```python
bank.tx.Send func

```

Note: IDEs should recognize the types and auto-fill the sdk module hierarchy, and the corresponding fields for the request and response objects for each method: IntelliJ, VS, WebStorm, PhpStorm, etc.
-->

## with_transactions()

_Wrap multiple messages in a single transaction._

```python
await sdk.db.with_transactions(
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
    metadata=None,
    credentials=None,
    wait_for_ready=True,
    compression=False,
    memo="optionalMemo",
)
```

Note: if any one of the messages fail in the function passed to withTransaction, then all messages will fail and not be committed to a block

# CRUD (db) module methods

- **Transactions**
  - **<a href="#Create">Create(kwargs) </a>**
  - **<a href="#Delete">Delete(kwargs) </a>**
  - **<a href="#DeleteAll">DeleteAll(kwargs) </a>**
  - **<a href="#MultiUpdate">MultiUpdate(kwargs) </a>**
  - **<a href="#Rename">Rename(kwargs) </a>**
  - **<a href="#RenewLease">RenewLease(kwargs) </a>**
  - **<a href="#RenewLeasesAll">RenewLeasesAll(kwargs) </a>**
  - **<a href="#Update">Update(kwargs) </a>**
  - **<a href="#Upsert">Upsert(kwargs) </a>**
- **Queries**
  - **<a href="#Count">Count(kwargs) </a>**
  - **<a href="#GetLease">GetLease(kwargs) </a>**
  - **<a href="#GetNShortestLeases">GetNShortestLeases(kwargs) </a>**
  - **<a href="#Has">Has(kwargs) </a>**
  - **<a href="#Keys">Keys(kwargs) </a>**
  - **<a href="#KeyValues">KeyValues(kwargs) </a>**
  - **<a href="#MyKeys">MyKeys(kwargs) </a>**
  - **<a href="#Read">Read(kwargs) </a>**
  - **<a href="#Search">Search(kwargs) </a>**

## Transactions

### Create(MsgCreateRequest) <a id="Create"></a>

Create a key-value in the database.

```python
await sdk.db.tx.Create(
    MsgCreate(
        creator=sample_creator,
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
```

Returns: MsgCreateResponse (empty object)

| MsgCreateRequest | Description         | Type     |
| :--------------- | :------------------ | -------- |
| creator          | Signer address      | str      |
| uuid             | Database identifier | str      |
| key              |                     | str      |
| value            |                     | bytes    |
| metadata         |                     | bytes    |
| lease            | Key-value life-span | Lease * |

\*Lease(seconds= number, minutes= number, hours= number, days= number, years= number)

- ### Delete(MsgDeleteRequest)<a id="Delete"></a>

Delete a key-value in the database.

```python
await sdk.db.tx.Delete(
    MsgDelete(creator=sample_creator, uuid="myUuid", key="myKey"),
    timeout=3000,
    metadata=None,
    credentials=None,
    wait_for_ready=True,
    compression=False,
)
```

Returns: MsgDeleteResponse (empty object)

| MsgDeleteRequest | Description         | Type |
| :--------------- | :------------------ | ---- |
| creator          | Signer address      | str  |
| uuid             | Database identifier | str  |
| key              | Key to delete       | str  |

- ### DeleteAll(MsgDeleteAllRequest)<a id="DeleteAll"></a>

Renew all the leases of key-values in the specified uuid.

```python
response = await sdk.db.tx.DeleteAll(creator=sample_creator, uuid="myUuid")
print(response)
```

Returns: Promise=>MsgDeleteAllResponse (empty object)

| MsgDeleteAllRequest | Description         | Type |
| :------------------ | :------------------ | ---- |
| creator             | Signer address      | str  |
| uuid                | Database identifier | str  |

- ### MultiUpdate(MsgMultiUpdateRequest)<a id="MultiUpdate"></a>

Update a set of key-values in the specified uuid.

```python
await sdk.db.tx.MultiUpdate(
    creator=sample_creator,
    uuid="myUuid",
    keyValues=[
        MsgUpdate(
            creator=sample_creator,
            uuid="uuid",
            key="myKey-1",
            value="updatedValue-2".encode("utf-8"),
            lease=Lease(minutes=1),
        ),
        MsgUpdate(
            creator=sample_creator,
            uuid="uuid",
            key="myKey-2",
            value="updatedValue-2".encode("utf-8"),
            lease=Lease(minutes=1),
        ),
    ],
)
```

Returns: MsgMultiUpdateResponse (empty object)

| MsgMultiUpdateRequest | Description                                         | Type             |
| :-------------------- | :-------------------------------------------------- | ---------------- |
| creator               | Signer address                                      | string           |
| uuid                  | Database identifier                                 | string           |
| keyValues             | KeyValueLease(key: str, value: bytes, lease: Lease) | KeyValueLease \[\] |

- ### Rename(MsgRenameRequest)<a id="Rename"></a>

Renew the lease of a key-value in the database.

```python
await sdk.db.tx.Rename(
    MsgRename(
        creator=sample_creator, uuid="myUuid", key="existingKey", newKey="renamingKey"
    ),
    timeout=3000,
    metadata=None,
    credentials=None,
    wait_for_ready=True,
    compression=False,
)
```

Returns: MsgRenameResponse (empty object)

| MsgRenameRequest | Description            | Type |
| :--------------- | :--------------------- | ---- |
| creator          | Signer address         | str  |
| uuid             | Database identifier    | str  |
| key              | Existing key           | str  |
| newKey           | New key used to rename | str  |

- ### RenewLease(MsgRenewLeaseRequest)<a id="RenewLease"></a>

Renew the lease of a key-value in the database.

```python
respons = await sdk.db.tx.RenewLease(
    MsgRenewLease(
        creator=sample_creator, uuid="myUuid", key="existingKey", lease=Lease(hours=1)
    ),
    timeout=3000,
    metadata=None,
    credentials=None,
    wait_for_ready=True,
    compression=False,
)
```

Returns: MsgRenewLeaseResponse (empty object)

| MsgRenewLeaseRequest | Description                 | Type     |
| :------------------- | :-------------------------- | -------- |
| creator              | Signer address              | str      |
| uuid                 | Database identifier         | str      |
| key                  |                             | str      |
| lease                | New life-span for key-value | Lease * |

\*Lease(seconds=number, minutes=number, hours=number, days=number, years=number)

- ### RenewLeasesAll(MsgRenewLeasesAllRequest)<a id="RenewLeasesAll"></a>

Renew all the leases of key-values in the specified uuid.

```python
await sdk.db.tx.RenewLeasesAll(
    MsgRenewLeasesAll(
        creator=sample_creator,
        uuid=uuid,
        lease=Lease(seconds=10),
    ),
    timeout=3000,
    metadata=None,
    credentials=None,
    wait_for_ready=True,
    compression=False,
)
```

Returns: MsgRenewLeasesAllResponse (empty object)

| MsgRenewLeasesAllRequest | Description                      | Type     |
| :----------------------- | :------------------------------- | -------- |
| creator                  | Signer address                   | str      |
| uuid                     | Database identifier              | str      |
| lease                    | New life-span for all key-values | Lease * |

\*Lease(seconds=number, minutes=number, hours=number, days=number, years=number)

- ### Update(MsgUpdateRequest)<a id="Update"></a>

Update a key-value in the database.

```python
await sdk.db.tx.Update(
    MsgUpdate(
        creator=sample_creator,
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
```

Returns: MsgUpdateResponse (empty object)

| MsgUpdateRequest | Description            | Type       |
| :--------------- | :--------------------- | ---------- |
| creator          | Signer address         | str        |
| uuid             | Database identifier    | str        |
| key              |                        | str        |
| value            | New value to update to | bytes      |
| metadata         |                        | bytes      |
| lease            | Key-value life-span    | Lease      |

\*Lease(seconds=number, minutes=number, hours=number, days=number, years=number)

- ### Upsert(MsgUpsertRequest)<a id="Upsert"></a>

Upsert a key-value in the database: create a key-value if the key doesn't exist, update the key-value if the key exists

```python
await sdk.db.tx.Upsert(
    MsgUpsert(
        creator=sample_creator,
        uuid="myUuid",
        key="keyToUpsert",
        value="valueToUpsert".encode("utf-8"),
    ),
    timeout=3000,
    metadata=None,
    credentials=None,
    wait_for_ready=True,
    compression=False,
)
```

Returns: MsgUpsertResponse (empty object)

| MsgUpsertRequest | Description         | Type       |
| :--------------- | :------------------ | ---------- |
| creator          | Signer address      | str        |
| uuid             | Database identifier | str        |
| key              |                     | str        |
| value            |                     | bytes      |
| metadata         |                     | bytes      |
| lease            | Key-value life-span | Lease *   |

\*Lease(seconds=number, minutes=number, hours=number, days=number, years=number)

## Queries

- ### Count(QueryCountRequest)<a id="Count"></a>

Query the total number of key-values in the specified uuid.

```python
await sdk.db.q.Count(
    MsgCount(uuid="myUuid"),
    timeout=3000,
    metadata=None,
    credentials=None,
    wait_for_ready=True,
    compression=False,
)
```

Returns: QueryCountResponse

| QueryCountRequest | Description         | Type   |
| :---------------- | :------------------ | ------ |
| uuid              | Database identifier | str    |

| QueryCountResponse | Description                      | Type   |
| :----------------- | :------------------------------- | ------ |
| count              | Number of key-values in the uuid | int    |

- ### GetLease(QueryGetLeaseRequest)<a id="GetLease"></a>

Get the remaining lease time of a key-value.

```python
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
```

Returns: QueryGetLeaseResponse

| QueryGetLeaseRequest | Description         | Type   |
| :------------------- | :------------------ | ------ |
| uuid                 | Database identifier | str    |
| key                  |                     | str    |

| QueryGetLeaseResponse | Description                       | Type   |
| :-------------------- | :-------------------------------- | ------ |
| seconds               | Remaining lease time of key-value | number |

- ### GetNShortestLeases(QueryGetNShortestLeasesRequest)<a id="GetNShortestLeases"></a>

Get the remaining lease time of a n key-values.

```python
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
```

Returns: QueryGetNShortestLeasesResponse

| QueryGetNShortestLeasesRequest | Description                   | Type   |
| :----------------------------- | :---------------------------- | ------ |
| uuid                           | Database identifier           | str    |
| num                            | Number of keyLeases to return | int    |

| QueryGetNShortestLeasesResponse | Description                             | Type            |
| :------------------------------ | :-------------------------------------- | --------------- |
| keyLeases                       | KeyLease(key=string, seconds=number)    |  list(KeyLease) |

- ### Has(QueryHasRequest)<a id="Has"></a>

Check if a key exists in the specified uuid.

```python
await sdk.db.q.Has(
  MsgHas((uuid = "myUuid"), (key = "myKey")),
  (timeout = 3000),
  (metadata = None),
  (credentials = None),
  (wait_for_ready = True),
  (compression = False)
);
```

Returns: QueryHasResponse

| QueryHasRequest | Description         | Type   |
| :-------------- | :------------------ | ------ |
| uuid            | Database identifier | str    |
| key             |                     | str    |

| QueryHasResponse | Description                                 | Type    |
| :--------------- | :------------------------------------------ | ------- |
| has              | true if key exists in uuid; false otherwise | bool    |

- ### Keys(QueryKeysRequest}<a id="Keys"></a>

Read the complete set of keys in the specified uuid.
###hhio

```python
await sdk.db.q.Keys(
    MsgKeys(uuid="myUuid", pagination={"start": "key-a", "limit": 50}),
    timeout=3000,
    metadata=None,
    credentials=None,
    wait_for_ready=True,
    compression=False,
)
```

Returns: QueryKeysResponse

| QueryKeysRequest      | Description                                   | Type          |
| :-------------------- | :-------------------------------------------- | ------------- |
| uuid                  | Database identifier                           | str           |
| pagination (optional) | PagingRequest(startKey=string, limit=Long)    | PagingRequest |

| QueryKeysResponse     | Description                                   | Type           |
| :-------------------- | :-------------------------------------------- | -------------- |
| keys                  |                                               | list(str)      |
| pagination (optional) | PagingResponse {nextKey: string, total: Long} | PagingResponse |

- ### KeyValues(QueryKeyValuesRequest)<a id="KeyValues"></a>

Read the complete set of key-values in the specified uuid.

```python
response = await sdk.db.q.KeyValues(
    QueryKeyValuesRequest(uuid=uuid),
    timeout=3000,
    metadata=None,
    credentials=None,
    wait_for_ready=True,
    compression=False,
)
```

Returns: QueryKeyValuesResponse

| QueryKeyValuesRequest | Description                                   | Type          |
| :-------------------- | :-------------------------------------------- | ------------- |
| uuid                  | Database identifier                           | str           |
| pagination (optional) | PagingRequest {startKey: string, limit: Long} | PagingRequest |

| QueryKeyValuesResponse | Description                                   | Type           |
| :--------------------- | :-------------------------------------------- | -------------- |
| keyValues              | KeyValue {key: string, value: Uint8Array}     | list(KeyValue) |
| pagination (optional)  | PagingResponse {nextKey: string, total: Long} | PagingResponse |

- ### MyKeys(QueryMyKeysRequest)<a id="MyKeys"></a>

Read the complete set of keys by address in the specified uuid.
###hhio

```python
await sdk.db.q.Keys(
  MsgKeys((uuid = "myUuid"), (address = sample_creator)),
  (timeout = 3000),
  (metadata = None),
  (credentials = None),
  (wait_for_ready = True),
  (compression = False)
);
```

Returns: QueryMyKeysResponse

| QueryMyKeysRequest    | Description                                   | Type          |
| :-------------------- | :-------------------------------------------- | ------------- |
| uuid                  | Database identifier                           | str           |
| address               | Bluzelle address                              | str           |
| pagination (optional) | PagingRequest {startKey: string, limit: Long} | PagingRequest |

| QueryMyKeysResponse   | Description                                   | Type           |
| :-------------------- | :-------------------------------------------- | -------------- |
| keys                  |                                               |  list(string)  |
| pagination (optional) | PagingResponse {nextKey: string, total: Long} | PagingResponse |

- ### Read(QueryReadRequest)<a id="Read"></a>

Read a value from the database.

```python
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
```

Returns: QueryReadResponse

| QueryReadRequest | Description         | Type   |
| :--------------- | :------------------ | ------ |
| uuid             | Database identifier | str    |
| key              |                     | str    |

| QueryReadResponse | Description | Type       |
| :---------------- | :---------- | ---------- |
| value             |             | bytes      |

- ### Search(QuerySearchRequest)<a id="Search"></a>

Search by key in the specified uuid.

```python
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
```

Returns: QuerySearchResponse

| QuerySearchRequest    | Description                                          | Type          |
| :-------------------- | :--------------------------------------------------- | ------------- |
| uuid                  | Database identifier                                  | str           |
| searchString          | query for keys that start with or match searchString | str           |
| pagination (optional) | {startKey: string, limit: Long}                      | PagingRequest |

| QuerySearchResponse   | Description                               | Type           |
| :-------------------- | :---------------------------------------- | -------------- |
| keyValues             | KeyValue {key: string, value: Uint8Array} | list(KeyValue) |
| pagination (optional) | {nextKey: string, total: Long}            | PagingResponse |
