import sys

if sys.version_info < (3, 8):
    from typing_extensions import Literal
else:
    from typing import Literal


# Valid transaction broadcast modes for the `POST /txs` endpoint of the
# Cosmos REST API.
SyncMode = Literal["sync", "async", "block"]


class Wallet:
    seed: str
    derivation_path: str
    private_key: bytes
    public_key: bytes
    address: str
