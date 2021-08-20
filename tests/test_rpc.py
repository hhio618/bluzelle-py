from base64 import b64encode

from bluzelle.codec.cosmos.bank.v1beta1.query_pb2 import QueryBalanceRequest
from bluzelle.codec.cosmos.base.v1beta1.coin_pb2 import Coin

# tender mint client test
from bluzelle.codec.crud.lease_pb2 import Lease
from bluzelle.codec.crud.query_pb2 import QueryReadRequest
from bluzelle.codec.crud.tx_pb2 import MsgCreate, MsgUpdate
from bluzelle.sdk.bluzelle import Bluzelle
from bluzelle.tendermint import Tendermint34Client

balance = Coin(denom=b"ubnt", amount=b"99946246")


class Tendermint34ClientMock(Tendermint34Client):
    def call(self, method, params):
        # Handle methods with empty params, like the `status` method.
        if len(params) == 0:
            # Status request
            if method == "status":
                return {
                    "node_info": {
                        "protocol_version": {"p2p": "8", "block": "11", "app": "0"},
                        "id": "dd6bdd834b480e4670adc06ff41e478b2b6899ac",
                        "listen_addr": "tcp://0.0.0.0:26656",
                        "network": "bluzelleTestNetPrivate-136",
                        "version": "",
                        "channels": "40202122233038606100",
                        "moniker": "daemon-sentry-client-0",
                        "other": {"tx_index": "on", "rpc_address": "tcp://0.0.0.0:26657"},
                    },
                    "sync_info": {
                        "latest_block_hash": "88C00DCA610770EEEF475A07BE375E0C5C0C83CF42AAC5DACA4136DDCFB742EE",
                        "latest_app_hash": "C93E0B09DD15A76F052C750CF39468A74C0F075D1540856BE138398CBDD54F45",
                        "latest_block_height": "887159",
                        "latest_block_time": "2021-08-19T11:37:31.583494239Z",
                        "earliest_block_hash": "FD30FE3F7B66849909AAE75CE9AED74C450FF56BA45DE4A36D6E21DBE68411E6",
                        "earliest_app_hash": "E3B0C44298FC1C149AFBF4C8996FB92427AE41E4649B934CA495991B7852B855",
                        "earliest_block_height": "1",
                        "earliest_block_time": "2021-06-24T05:17:06.882537818Z",
                        "catching_up": False,
                    },
                    "validator_info": {
                        "address": "82D64671259A37F9DE58539AE649DEDC521BEA55",
                        "pub_key": {
                            "type": "tendermint/PubKeyEd25519",
                            "value": "zTvxYkXohKTHV+4+Bcq9HrtBo0JcVt2ZUphhYdYSMCI=",
                        },
                        "voting_power": "0",
                    },
                }

        elif "data" in params:
            # Account read request
            if (
                params["data"]
                == "0a2f626c757a656c6c6531716c6d65346b3667647277323576756573396b637a336e6d3677386333386d6c38326b7a356b"
            ):
                return {
                    "response": {
                        "code": 0,
                        "log": "",
                        "info": "",
                        "index": "0",
                        "key": None,
                        "value": "CqIBCiAvY29zbW9zLmF1dGgudjFiZXRhMS5CYXNlQWNjb3VudBJ+Ci9ibHV6ZWxsZTFxbG1lNGs2Z2RydzI1dnVlczlrY3ozbm02dzhjMzhtbDgya3o1axJGCh8vY29zbW9zLmNyeXB0by5zZWNwMjU2azEuUHViS2V5EiMKIQOLGQ/0dl4IOUFJdWUP0NV1bRSaiwl772m+w7PAQXLdyBi+AiB/",
                        "proofOps": None,
                        "height": "887159",
                        "codespace": "",
                    }
                }
            # Balance request
            elif params["data"] == "0a0e73616d706c655f63726561746f72120475626e74":
                value = balance.SerializeToString()
                value = b"\n\x10" + value
                return {
                    "response": {
                        "code": 0,
                        "log": "",
                        "info": "",
                        "index": "0",
                        "key": None,
                        "value": b64encode(value).decode("utf-8"),
                        "proofOps": None,
                        "height": "860035",
                        "codespace": "",
                    }
                }
            # Read request
            elif params["data"] == "0a0a64756d6d792d7575696412056d794b6579":
                return {
                    "response": {
                        "code": 0,
                        "log": "",
                        "info": "",
                        "index": "0",
                        "key": None,
                        "value": "CgdteVZhbHVl",
                        "proofOps": None,
                        "height": "855811",
                        "codespace": "",
                    }
                }
        # If it's a tx search request.
        elif "query" in params:
            # Dummy create response
            if (
                "C32C2FEA3F9E7B592C7EA1449356BF2CB3280423AA6BF20B9D5954D38ACC6143"
                in params["query"]
            ):
                return {
                    "txs": [
                        {
                            "hash": "C32C2FEA3F9E7B592C7EA1449356BF2CB3280423AA6BF20B9D5954D38ACC6143",
                            "height": "888463",
                            "index": 0,
                            "tx_result": {
                                "code": 0,
                                "data": "CggKBkNyZWF0ZQ==",
                                "log": '[{"events":[{"type":"message","attributes":[{"key":"action","value":"Create"}]}]}]',
                                "info": "",
                                "gas_wanted": "100000000",
                                "gas_used": "185172",
                                "events": [
                                    {
                                        "type": "message",
                                        "attributes": [
                                            {"key": "YWN0aW9u", "value": "Q3JlYXRl", "index": True}
                                        ],
                                    }
                                ],
                                "codespace": "",
                            },
                            "tx": "CpEBCo4BCh8vYmx1emVsbGUuY3VyaXVtLmNydWQuTXNnQ3JlYXRlEmsKL2JsdXplbGxlMXFsbWU0azZnZHJ3MjV2dWVzOWtjejNubTZ3OGMzOG1sODJrejVrEiQ4ODVmNmY5Zi0zZTI1LTQ3OWQtOGZiOS1mYmZiNmJlZmNkMDkaBW15S2V5IgdteVZhbHVlKgIYARJqClEKRgofL2Nvc21vcy5jcnlwdG8uc2VjcDI1NmsxLlB1YktleRIjCiEDixkP9HZeCDlBSXVlD9DVdW0UmosJe+9pvsOzwEFy3cgSBAoCCAEYjAESFQoOCgR1Ym50EgYyMDAwMDAQgMLXLxpAR4ULr4rqCbxkyHajz1pU+IePd2YXmEAuBAlE/FkD9V9ny0dtESwi1Iby7Wgwt2BLd5NbLq23sgEClOUPQER/cA==",
                            "proof": {
                                "root_hash": "C654C8C6BF3AD02F4619CA7E55C535724B48EC24AA2558AD8F5F36C3EE91712E",
                                "data": "CpEBCo4BCh8vYmx1emVsbGUuY3VyaXVtLmNydWQuTXNnQ3JlYXRlEmsKL2JsdXplbGxlMXFsbWU0azZnZHJ3MjV2dWVzOWtjejNubTZ3OGMzOG1sODJrejVrEiQ4ODVmNmY5Zi0zZTI1LTQ3OWQtOGZiOS1mYmZiNmJlZmNkMDkaBW15S2V5IgdteVZhbHVlKgIYARJqClEKRgofL2Nvc21vcy5jcnlwdG8uc2VjcDI1NmsxLlB1YktleRIjCiEDixkP9HZeCDlBSXVlD9DVdW0UmosJe+9pvsOzwEFy3cgSBAoCCAEYjAESFQoOCgR1Ym50EgYyMDAwMDAQgMLXLxpAR4ULr4rqCbxkyHajz1pU+IePd2YXmEAuBAlE/FkD9V9ny0dtESwi1Iby7Wgwt2BLd5NbLq23sgEClOUPQER/cA==",
                                "proof": {
                                    "total": "1",
                                    "index": "0",
                                    "leaf_hash": "xlTIxr860C9GGcp+VcU1cktI7CSqJVitj182w+6RcS4=",
                                    "aunts": [],
                                },
                            },
                        }
                    ],
                    "total_count": "1",
                }
            # Dummy update response
            elif (
                "2EB26782D3EE9C0E9DEC09033A6C5B77A83C1592F7C505BC8D1DBDB6485A1025"
                in params["query"]
            ):
                return {
                    "txs": [
                        {
                            "hash": "2EB26782D3EE9C0E9DEC09033A6C5B77A83C1592F7C505BC8D1DBDB6485A1025",
                            "height": "888463",
                            "index": 0,
                            "tx_result": {
                                "code": 0,
                                "data": "CggKBkNyZWF0ZQ==",
                                "log": '[{"events":[{"type":"message","attributes":[{"key":"action","value":"Create"}]}]}]',
                                "info": "",
                                "gas_wanted": "100000000",
                                "gas_used": "185172",
                                "events": [
                                    {
                                        "type": "message",
                                        "attributes": [
                                            {"key": "YWN0aW9u", "value": "Q3JlYXRl", "index": True}
                                        ],
                                    }
                                ],
                                "codespace": "",
                            },
                            "tx": "CpEBCo4BCh8vYmx1emVsbGUuY3VyaXVtLmNydWQuTXNnQ3JlYXRlEmsKL2JsdXplbGxlMXFsbWU0azZnZHJ3MjV2dWVzOWtjejNubTZ3OGMzOG1sODJrejVrEiQ4ODVmNmY5Zi0zZTI1LTQ3OWQtOGZiOS1mYmZiNmJlZmNkMDkaBW15S2V5IgdteVZhbHVlKgIYARJqClEKRgofL2Nvc21vcy5jcnlwdG8uc2VjcDI1NmsxLlB1YktleRIjCiEDixkP9HZeCDlBSXVlD9DVdW0UmosJe+9pvsOzwEFy3cgSBAoCCAEYjAESFQoOCgR1Ym50EgYyMDAwMDAQgMLXLxpAR4ULr4rqCbxkyHajz1pU+IePd2YXmEAuBAlE/FkD9V9ny0dtESwi1Iby7Wgwt2BLd5NbLq23sgEClOUPQER/cA==",
                            "proof": {
                                "root_hash": "C654C8C6BF3AD02F4619CA7E55C535724B48EC24AA2558AD8F5F36C3EE91712E",
                                "data": "CpEBCo4BCh8vYmx1emVsbGUuY3VyaXVtLmNydWQuTXNnQ3JlYXRlEmsKL2JsdXplbGxlMXFsbWU0azZnZHJ3MjV2dWVzOWtjejNubTZ3OGMzOG1sODJrejVrEiQ4ODVmNmY5Zi0zZTI1LTQ3OWQtOGZiOS1mYmZiNmJlZmNkMDkaBW15S2V5IgdteVZhbHVlKgIYARJqClEKRgofL2Nvc21vcy5jcnlwdG8uc2VjcDI1NmsxLlB1YktleRIjCiEDixkP9HZeCDlBSXVlD9DVdW0UmosJe+9pvsOzwEFy3cgSBAoCCAEYjAESFQoOCgR1Ym50EgYyMDAwMDAQgMLXLxpAR4ULr4rqCbxkyHajz1pU+IePd2YXmEAuBAlE/FkD9V9ny0dtESwi1Iby7Wgwt2BLd5NbLq23sgEClOUPQER/cA==",
                                "proof": {
                                    "total": "1",
                                    "index": "0",
                                    "leaf_hash": "xlTIxr860C9GGcp+VcU1cktI7CSqJVitj182w+6RcS4=",
                                    "aunts": [],
                                },
                            },
                        }
                    ],
                    "total_count": "1",
                }

        # If it's transaction request.
        elif "tx" in params:
            # Responding to the sample MsgCreate request.
            if (
                bytes(params["tx"])
                == b'\nU\nS\n\x1f/bluzelle.curium.crud.MsgCreate\x120\n\x0esample_creator\x12\ndummy-uuid\x1a\x05myKey"\x07myValue*\x02\x18\x01\x12i\nP\nF\n\x1f/cosmos.crypto.secp256k1.PubKey\x12#\n!\x03\x8b\x19\x0f\xf4v^\x089AIue\x0f\xd0\xd5um\x14\x9a\x8b\t{\xefi\xbe\xc3\xb3\xc0Ar\xdd\xc8\x12\x04\n\x02\x08\x01\x18\x7f\x12\x15\n\x0e\n\x04ubnt\x12\x06200000\x10\x80\xc2\xd7/\x1a@\x17\xfcmQ\xd3^\x8d\xde\xf1\x96\tA\x90\xb0o\xa2`\x95R\xfa\nX\x08-\x12>\xd4\x99\xadmn&V\xe0\xb1y\x17\x94\x7fOU\xa1-\x9b\xa8\xc1\x17\x9b*\x9a\xbaR\x07u\xc4\xbc\xd8Ka\xa9R\xc3\x03\xab'
            ):
                return {
                    "code": 0,
                    "data": "",
                    "log": "[]",
                    "codespace": "",
                    "hash": "C32C2FEA3F9E7B592C7EA1449356BF2CB3280423AA6BF20B9D5954D38ACC6143",
                }

            # Responding to the sample MsgUpdate request.
            elif (
                bytes(params["tx"])
                == b'\nZ\nX\n\x1f/bluzelle.curium.crud.MsgUpdate\x125\n\x0esample_creator\x12\ndummy-uuid\x1a\x05myKey"\x0cupdatedValue*\x02\x10\x01\x12i\nP\nF\n\x1f/cosmos.crypto.secp256k1.PubKey\x12#\n!\x03\x8b\x19\x0f\xf4v^\x089AIue\x0f\xd0\xd5um\x14\x9a\x8b\t{\xefi\xbe\xc3\xb3\xc0Ar\xdd\xc8\x12\x04\n\x02\x08\x01\x18\x7f\x12\x15\n\x0e\n\x04ubnt\x12\x06200000\x10\x80\xc2\xd7/\x1a@?~/>\x8f\xa4[F\x80\xf0\xc7kB\x93\xd4\x9e(\x0b;\x07\xf0w\x91M\x9aB[i\x936%\x91hN\xa9\x93\x8f6\xa1\xfd\x13|\x9c&T\thVn\xfb\xc5\xa5\x88\x8e\xbe\x89\xc3(\xce\xf9,\x1e\xba\xec'
            ):
                return {
                    "code": 0,
                    "data": "",
                    "log": "[]",
                    "codespace": "",
                    "hash": "2EB26782D3EE9C0E9DEC09033A6C5B77A83C1592F7C505BC8D1DBDB6485A1025",
                }

        return None


class MockBluzelle(Bluzelle):
    def create_tendermint_client(self, host, port, logging_level):
        return Tendermint34ClientMock(host, port)


uuid = "dummy-uuid"


class TestRpc:
    def setup(self):
        self.sdk = MockBluzelle(
            mnemonic="space dilemma domain payment snap crouch arrange"
            " fantasy draft shaft fitness rain habit dynamic tip "
            "faith mushroom please power kick impulse logic wet cricket",
            host="https://test.com",
            port=1111,
            max_gas=100000000,
            gas_price=0.002,
        )

    async def test_create_transaction(self):
        sample_creator = "sample_creator"
        response = await self.sdk.db.tx.Create(
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
        assert (
            response["txs"][0]["hash"]
            == "C32C2FEA3F9E7B592C7EA1449356BF2CB3280423AA6BF20B9D5954D38ACC6143"
        )

    async def test_read_transaction(self):
        response = await self.sdk.db.q.Read(
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
        assert response.value == b"myValue"

    async def test_update_transaction(self):
        sample_creator = "sample_creator"
        response = await self.sdk.db.tx.Update(
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
        assert (
            response["txs"][0]["hash"]
            == "2EB26782D3EE9C0E9DEC09033A6C5B77A83C1592F7C505BC8D1DBDB6485A1025"
        )

    async def test_query_balance_request(self):
        sample_creator = "sample_creator"
        response = await self.sdk.bank.q.Balance(
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
        assert response.balance.amount == balance.amount
