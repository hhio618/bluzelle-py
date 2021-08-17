from unittest import mock

from bluzelle.cosmos import generate_wallet, privkey_to_address, privkey_to_pubkey, seed_to_privkey
from bluzelle.cosmos.typing import Wallet
# come from create

from bluzelle.tendermint import Tendermint34Client


# tender mint client test
class Tendermint34ClientMock(Tendermint34Client):
    def call(self, method, params):
        if method == 'create':
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
        if method == 'read':
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

        return None


def test_create_transaction():
    tender_client = Tendermint34ClientMock(host='testnet.com', port=1212)
    response = tender_client.call(method='create', params={
        'key': "myKey",
        'value': "myValue".encode("utf-8"),
    })
    assert int(response['result']['total_count']) == 1


def test_read_transaction():
    tender_client = Tendermint34ClientMock(host='testnet.com', port=1212)
    # if the value is equal to myValue as in create test case example, then the result hash should be the same
    response = tender_client.call(method='read', params={
        'key': "myKey",
    })
    assert response['result']['response']['value'] == 'CgdteVZhbHVl'



# wallet tests

test_vector: Wallet = {
    "seed": "todo",
    "derivation_path": "todo",
    "private_key": bytes.fromhex(
        "8088c2ed2149c34f6d6533b774da4e1692eb5cb426fdbaef6898eeda489630b7"
    ),
    "public_key": bytes.fromhex(
        "02ba66a84cf7839af172a13e7fc9f5e7008cb8bca1585f8f3bafb3039eda3c1fdd"
    ),
    "address": "bluzelle1r5v5srda7xfth3hn2s26txvrcrntldjuwnye3w",
}

seed_test_vector: Wallet = {
    "seed": "teach there dream chase fatigue abandon lava super senior artefact close upgrade",
    "derivation_path": "m/44'/118'/0'/0/0",
    "private_key": bytes.fromhex(
        "8d0a8d165cf26d7a6f2dd621ed2fd9ebdb9596281906e48115f80164c0a64e1d"
    ),
    "public_key": bytes.fromhex(
        "036abfed6c95453a552160ca41487d42aafdbcd02aa62074056cc30cca2ea497a4"
    ),
    "address": "bluzelle1r5v5srda7xfth3hn2s26txvrcrntldjuwnye3w",
}


def test_seed_to_privkey():
    assert (
        seed_to_privkey(seed_test_vector["seed"], path=seed_test_vector["derivation_path"])
        == seed_test_vector["private_key"]
    )


def test_privkey_to_pubkey():
    assert privkey_to_pubkey(test_vector["private_key"]) == test_vector["public_key"]


def test_privkey_to_address():
    print(privkey_to_address(test_vector["private_key"]))
    assert privkey_to_address(test_vector["private_key"]) == test_vector["address"]


def test_generate_wallet():
    with mock.patch("os.urandom") as mock_urandom:
        mock_urandom.return_value = b"\x1e\xd2\x7f9\xa7\x0em\xfd\xa0\xb4\xaa\xc4\x0b\x83\x0e%\xbf\xe6DG\x7f:a\xe6#qa\x1ch5D\xa9"  # noqa: E501
        expected_wallet = {
            "seed": "burst negative solar evoke traffic yard lizard next series foster seminar enter wrist captain bulb trap giggle country sword season shoot boy bargain deal",  # noqa: E501
            "derivation_path": "m/44'/118'/0'/0/0",
            "private_key": bytes.fromhex(
                "bb8ac5bf9c342852fa5943d1366375c6f985d4601e596f23c5a49d095bfb2878"
            ),
            "public_key": bytes.fromhex(
                "03a7cc51198fc666901ec7b627926dad0c85d128ebe3251a132f009dcde1d64e03"
            ),
            "address": "bluzelle1dep39rnnwztpt63jx0htxrkt3lgku2cdkvrlgh",
        }
        assert generate_wallet() == expected_wallet



