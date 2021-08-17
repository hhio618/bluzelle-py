
from bluzelle.tendermint import Tendermint34Client
import uuid as u

# tender mint client test
from bluzelle.codec.crud.lease_pb2 import Lease
from bluzelle.codec.crud.tx_pb2 import MsgCreate, MsgUpdate
from bluzelle.codec.crud.query_pb2 import QueryReadRequest
from bluzelle.codec.cosmos.bank.v1beta1.query_pb2 import QueryBalanceRequest


class Tendermint34ClientMock(Tendermint34Client):
    def call(self, method, params):
        if type(method).__name__ == 'MsgCreate':
            return {'jsonrpc': '2.0', 'id': '3',
                    'result': {'txs': [
                        {'hash': '823D6F46BE65C9AAF47A6045AD427DEC749C72103B09DCAFC96FD4FFDE4E631F',
                         'height': '855612', 'index': 0,
                         'tx_result': {'code': 0, 'data': 'CggKBkNyZWF0ZQ==',
                                       'log': '[{"events":[{"type":"message","attributes":[{"key":"action","value":"Create"}]}]}]',
                                       'info': '', 'gas_wanted': '100000000', 'gas_used': '185120',
                                       'events': [{'type': 'message', 'attributes': [
                                           {'key': 'YWN0aW9u', 'value': 'Q3JlYXRl', 'index': True}]
                                                   }], 'codespace': ''},
                         'tx': 'CpEBCo4BCh8vYmx1emVsbGUuY3VyaXVtLmNydWQuTXNnQ3JlYXRlEmsKL2JsdXplbGxlMXFsbWU0azZnZHJ3MjV2dWVzOWtjejNubTZ3OGMzOG1sODJrejVrEiQ3N2EwNzJhNC1kNjZjLTQyMjgtYTI5NS03NjQ4YjVjOWMyNzYaBW15S2V5IgdteVZhbHVlKgIYARJpClAKRgofL2Nvc21vcy5jcnlwdG8uc2VjcDI1NmsxLlB1YktleRIjCiEDixkP9HZeCDlBSXVlD9DVdW0UmosJe+9pvsOzwEFy3cgSBAoCCAEYdhIVCg4KBHVibnQSBjIwMDAwMBCAwtcvGkC0KPjvmz8N+k57q02aFBHfIe/6UB9JKCjTLVTyYEoMFTpCn0dcjas97knhLCOVvwivXPtMUJfb8oSh/V0KJK3K',
                         'proof': {'root_hash': '1893CD73FECA803A5385E6F7585EEAA83B66F1488CA82F4CD3DF53A85208D6FC',
                                   'data': 'CpEBCo4BCh8vYmx1emVsbGUuY3VyaXVtLmNydWQuTXNnQ3JlYXRlEmsKL2JsdXplbGxlMXFsbWU0azZnZHJ3MjV2dWVzOWtjejNubTZ3OGMzOG1sODJrejVrEiQ3N2EwNzJhNC1kNjZjLTQyMjgtYTI5NS03NjQ4YjVjOWMyNzYaBW15S2V5IgdteVZhbHVlKgIYARJpClAKRgofL2Nvc21vcy5jcnlwdG8uc2VjcDI1NmsxLlB1YktleRIjCiEDixkP9HZeCDlBSXVlD9DVdW0UmosJe+9pvsOzwEFy3cgSBAoCCAEYdhIVCg4KBHVibnQSBjIwMDAwMBCAwtcvGkC0KPjvmz8N+k57q02aFBHfIe/6UB9JKCjTLVTyYEoMFTpCn0dcjas97knhLCOVvwivXPtMUJfb8oSh/V0KJK3K',
                                   'proof': {'total': '1', 'index': '0', 'leaf_hash': 'GJPNc/7KgDpTheb3WF7qqDtm8UiMqC9M099TqFII1vw=',
                                             'aunts': []}}}],
                        'total_count': '1'}}
        if type(method).__name__ == 'QueryReadRequest':
            return {
                    'jsonrpc': '2.0', 'id': '4',
                    'result': {
                            'response':
                            {
                                'code': 0,
                                'log': '',
                                'info': '',
                                'index': '0',
                                'key': None,
                                'value': 'CgdteVZhbHVl',
                                'proofOps': None,
                                'height': '855811',
                                'codespace': ''
                            }
                        }
                    }
        if type(method).__name__ == 'MsgUpdate':
            return {'jsonrpc': '2.0', 'id': '7',
                    'result': {'txs':
                                   [
                                       {
                                           'hash': '13EF6DB654ED13DE2ABFA652B386E542C755F7E1636D01380A1ED6BAEC97704C',
                                           'height': '859929', 'index': 0,
                                           'tx_result':
                                               {
                                                   'code': 0, 'data': 'ChEKD1VwZGF0ZUNydWRWYWx1ZQ==',
                                                   'log': '[{"events":[{"type":"message","attributes":[{"key":"action","value":"UpdateCrudValue"}]}]}]',
                                                   'info': '', 'gas_wanted': '100000000', 'gas_used': '50819',
                                                   'events': [{'type': 'message', 'attributes':
                                                       [
                                                           {'key': 'YWN0aW9u', 'value': 'VXBkYXRlQ3J1ZFZhbHVl', 'index': True}]}], 'codespace': ''},
                                           'tx': 'CpYBCpMBCh8vYmx1emVsbGUuY3VyaXVtLmNydWQuTXNnVXBkYXRlEnAKL2JsdXplbGxlMXFsbWU0azZnZHJ3MjV2dWVzOWtjejNubTZ3OGMzOG1sODJrejVrEiQ4ZWM0OTQwMS0xNDE2LTQ4MzUtOTZkNS0zYTdhY2M4NGQ2ODcaBW15S2V5Igx1cGRhdGVkVmFsdWUqAhABEmkKUApGCh8vY29zbW9zLmNyeXB0by5zZWNwMjU2azEuUHViS2V5EiMKIQOLGQ/0dl4IOUFJdWUP0NV1bRSaiwl772m+w7PAQXLdyBIECgIIARh6EhUKDgoEdWJudBIGMjAwMDAwEIDC1y8aQJQEVtdk4+NXz1ZCxZPTwOWAiJzWaRwrLdW+i+NCJzjdXIke9Vs4Dr7bEXE2bd1dc+kdFR9aC1IqKgsy6OIKuIM=',
                                           'proof': {'root_hash': '5339EFDC9F2AA2D0D53B671AD96B4B7B3EB58DC02CB25B4EAC771E09446E7530', 'data': 'CpYBCpMBCh8vYmx1emVsbGUuY3VyaXVtLmNydWQuTXNnVXBkYXRlEnAKL2JsdXplbGxlMXFsbWU0azZnZHJ3MjV2dWVzOWtjejNubTZ3OGMzOG1sODJrejVrEiQ4ZWM0OTQwMS0xNDE2LTQ4MzUtOTZkNS0zYTdhY2M4NGQ2ODcaBW15S2V5Igx1cGRhdGVkVmFsdWUqAhABEmkKUApGCh8vY29zbW9zLmNyeXB0by5zZWNwMjU2azEuUHViS2V5EiMKIQOLGQ/0dl4IOUFJdWUP0NV1bRSaiwl772m+w7PAQXLdyBIECgIIARh6EhUKDgoEdWJudBIGMjAwMDAwEIDC1y8aQJQEVtdk4+NXz1ZCxZPTwOWAiJzWaRwrLdW+i+NCJzjdXIke9Vs4Dr7bEXE2bd1dc+kdFR9aC1IqKgsy6OIKuIM=',
                                                     'proof': {'total': '1', 'index': '0', 'leaf_hash': 'Uznv3J8qotDVO2ca2WtLez61jcAssltOrHceCURudTA=', 'aunts': []}}}],
                        'total_count': '1'}}
        if type(method).__name__ == 'QueryBalanceRequest':
            return {'jsonrpc': '2.0', 'id': '4',
                    'result': {'response':
                                   {'code': 0, 'log': '', 'info': '', 'index': '0', 'key': None,
                                    'value': 'ChAKBHVibnQSCDk5OTQ2MjQ2', 'proofOps': None,
                                    'height': '860035', 'codespace': ''}}}

        return None


class Tx:
    def Create(self, msg_create, **kwargs):
        return Tendermint34ClientMock(host='testnet.com', port=1212).call(msg_create, params=kwargs)

    def Update(self, msg_create, **kwargs):
        return Tendermint34ClientMock(host='testnet.com', port=1212).call(msg_create, params=kwargs)


class Q:
    def Read(self, msg_create, **kwargs):
        return Tendermint34ClientMock(host='testnet.com', port=1212).call(msg_create, params=kwargs)

    def Balance(self, msg_create, **kwargs):
        return Tendermint34ClientMock(host='testnet.com', port=1212).call(msg_create, params=kwargs)


class Db:
    def __init__(self):
        self.tx = Tx()
        self.q = Q()


class Bank:
    def __init__(self):
        self.q = Q()


# sample mock SDK
class Bluzelle:
    def __init__(self):
        self.db = Db()
        self.bank = Bank()


class Create:
    def __init__(self, dict):
        self.key = dict['key']
        self.value = dict['value']
        self.uuid = 'uuid'


def test_create_transaction():
    sdk = Bluzelle()
    uuid = str(u.uuid4())
    sample_creator = 'sample_creator'
    response = sdk.db.tx.Create(
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
    assert int(response['result']['total_count']) == 1


def test_read_transaction():
    sdk = Bluzelle()
    uuid = str(u.uuid4())
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
    assert response['result']['response']['value'] == 'CgdteVZhbHVl'



def test_update_transaction():
    sdk = Bluzelle()
    uuid = str(u.uuid4())
    sample_creator = 'sample_creator'
    response = sdk.db.tx.Update(
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
    assert int(response['result']['total_count']) == 1


def test_query_balance_request():
    sdk = Bluzelle()
    sample_creator = 'sample_creator'
    response = sdk.bank.q.Balance(
        QueryBalanceRequest(
            address=sample_creator,
            denom="ubnt",
        ),
        timeout=3000,
        metadata=None,
        credentials=None,
        wait_for_ready=True,
        compression=False,
    )
    assert response['result']['response']['value'] == 'ChAKBHVibnQSCDk5OTQ2MjQ2'


