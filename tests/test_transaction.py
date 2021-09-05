import pytest

from bluzelle.codec.cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from bluzelle.codec.cosmos.base.v1beta1.coin_pb2 import Coin
from bluzelle.codec.cosmos.tx.signing.v1beta1.signing_pb2 import SIGN_MODE_DIRECT
from bluzelle.codec.cosmos.tx.v1beta1.tx_pb2 import Fee

# tender mint client test
from bluzelle.codec.crud.lease_pb2 import Lease
from bluzelle.codec.crud.tx_pb2 import MsgCreate
from bluzelle.cosmos import DirectSignModeHandler, Transaction

uuid = "dummy-uuid"
test_transaction = {
    "inputs": {
        "privkey": b"\x95|-Z\xbe.\x1f\\\xd8e\xc7?\xca\xc6\xb5D\xac~%Xd\xbeX\xf8\xd4\x85\xcd`\xcc\xa1\xb7#",
        "account": BaseAccount.FromString(
            b"\n/bluzelle1qlme4k6gdrw25vues9kcz3nm6w8c38ml82kz5k\x12F\n\x1f/cosmos.crypto.secp256k1.PubKey\x12#\n!\x03\x8b\x19\x0f\xf4v^\x089AIue\x0f\xd0\xd5um\x14\x9a\x8b\t{\xefi\xbe\xc3\xb3\xc0Ar\xdd\xc8\x18\xbe\x02 \xbb\x01"
        ),
        "messages": [
            MsgCreate(
                creator="sample_creator",
                uuid=uuid,
                key="myKey",
                value="myValue".encode("utf-8"),
                lease=Lease(hours=1),
            ),
        ],
        "memo": "mimo",
        "chain_id": "GVGHVY",
        "fee": Fee(
            gas_limit=100000000,
            amount=[Coin(denom="ubnt", amount="2000000")],
        ),
        "sign_mode": SIGN_MODE_DIRECT,
    },
    "sign_mode_handler": DirectSignModeHandler(),
    "raw_bytes": b'\n[\nS\n\x1f/bluzelle.curium.crud.MsgCreate\x120\n\x0esample_creator\x12\ndummy-uuid\x1a\x05myKey"\x07myValue*\x02\x18\x01\x12\x04mimo\x12k\nQ\nF\n\x1f/cosmos.crypto.secp256k1.PubKey\x12#\n!\x03\x8b\x19\x0f\xf4v^\x089AIue\x0f\xd0\xd5um\x14\x9a\x8b\t{\xefi\xbe\xc3\xb3\xc0Ar\xdd\xc8\x12\x04\n\x02\x08\x01\x18\xbb\x01\x12\x16\n\x0f\n\x04ubnt\x12\x072000000\x10\x80\xc2\xd7/\x1a\x06GVGHVY \xbe\x02',
    "signed_bytes": b"\x83\xe8\x0e\xdei\x8d4\xd8\xe1\xe8y\xd0z\xe2\xc3\xe7k\xf8\xd7@.\xc3\x07\xb0\xd8\\\xce\x95W\xc8\xe1\x81;0.-)\x05\xc3\xe5\xb1C-\x81B\xef\xa8!U\x92\xce\xb1\t\xbd\xf2:\x80*\x80\xa59\xef\x84G",
    "signatures": [
        b"\x83\xe8\x0e\xdei\x8d4\xd8\xe1\xe8y\xd0z\xe2\xc3\xe7k\xf8\xd7@.\xc3\x07\xb0\xd8\\\xce\x95W\xc8\xe1\x81;0.-)\x05\xc3\xe5\xb1C-\x81B\xef\xa8!U\x92\xce\xb1\t\xbd\xf2:\x80*\x80\xa59\xef\x84G"
    ],
}


class TestTransaction:
    def setup(self):
        self.tx = Transaction(**test_transaction["inputs"])
        self.raw_bytes = self.tx.create(sign_mode_handler=test_transaction["sign_mode_handler"])

    @pytest.mark.asyncio
    async def test_transaction_raw(self):
        assert self.raw_bytes == test_transaction["raw_bytes"]

    @pytest.mark.asyncio
    async def test_transaction_signed(self):
        assert self.tx._sign(self.raw_bytes) == test_transaction["signed_bytes"]

    @pytest.mark.asyncio
    async def test_transaction_data(self):
        tx_data = self.tx.sign(self.raw_bytes)
        assert tx_data.signatures == test_transaction["signatures"]
        assert tx_data.body.memo == test_transaction["inputs"]["memo"]
        assert tx_data.auth_info.fee == test_transaction["inputs"]["fee"]
        assert (
            tx_data.auth_info.signer_infos[0].sequence
            == test_transaction["inputs"]["account"].sequence
        )
