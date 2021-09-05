import base64

from google.protobuf import json_format
import pytest

from bluzelle.codec.tendermint.abci.types_pb2 import RequestQuery
from bluzelle.tendermint import Tendermint34Client


class MockTx:
    def SerializeToString(self):
        return "dummy"


@pytest.mark.asyncio
async def test_tendermint_send_func(mocker):
    tendermint: Tendermint34Client = Tendermint34Client("https://localhost", 1234)
    assert tendermint.send_request_func == tendermint.send_http_request
    tendermint: Tendermint34Client = Tendermint34Client("wss://localhost", 1234)
    assert tendermint.send_request_func == tendermint.send_wss_request


@pytest.mark.asyncio
async def test_tendermint_status(mocker):
    tendermint: Tendermint34Client = Tendermint34Client("https://localhost", 1234)
    tendermint.call = mocker.AsyncMock(return_value=None)
    tendermint.pb_invoke = mocker.AsyncMock(return_value=None)
    await tendermint.status()
    tendermint.call.assert_called_with("status", [])
    tendermint.pb_invoke.assert_not_called


@pytest.mark.asyncio
async def test_tendermint_abci_query(mocker):
    tendermint: Tendermint34Client = Tendermint34Client("https://localhost", 1234)
    tendermint.call = mocker.AsyncMock(return_value={"response": {"value": "dummy"}})
    await tendermint.abci_query("path", b"\x22\x33")
    req = RequestQuery(path="path", data=b"\x22\x33", height=None, prove=False)
    payload = json_format.MessageToDict(req)
    payload["data"] = base64.b64decode(payload["data"]).hex()
    tendermint.call.assert_called_with("abci_query", payload)


@pytest.mark.asyncio
async def test_tendermint_broadcast_tx_sync(mocker):
    tendermint: Tendermint34Client = Tendermint34Client("https://localhost", 1234)
    tendermint.call = mocker.AsyncMock(return_value=None)
    await tendermint.broadcast_tx_sync(tx=MockTx())
    tendermint.call.assert_called_with("broadcast_tx_sync", {"tx": list("dummy")})


@pytest.mark.asyncio
async def test_tendermint_tx_search(mocker):
    tendermint: Tendermint34Client = Tendermint34Client("https://localhost", 1234)
    tendermint.call = mocker.AsyncMock(return_value=None)
    await tendermint.tx_search(query="dummy")
    req = {
        "query": "dummy",
        "prove": True,
        "page": None,
        "per_page": None,
    }
    tendermint.call.assert_called_with("tx_search", req)
