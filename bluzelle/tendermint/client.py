

"""
TCP Server that communicates with Tendermint
"""
import asyncio
import signal
import platform
import json
import requests
import itertools
import base64
from bluzelle.utils import *
from io import BytesIO
from bluzelle.codec.tendermint.abci.types_pb2 import (
    Request,
    RequestInfo,
    RequestQuery,
    RequestCheckTx,
    Response,
    ResponseException,
    ResponseFlush,
    ResponseQuery,
    ResponseInfo,
)
from google.protobuf import json_format
from google.protobuf.message import Message

MaxReadInBytes = 64 * 1024  # Max we'll consume on a read stream

log = get_logger("Tendermint34Client")

AGENT='bluzelle-py/0.1'

# See https://github.com/davebryson/py-tendermint/blob/master/tendermint/client.py
class Tendermint34Client:
    def __init__(self, host: str, port: int):
        # Tendermint endpoint
        self.uri = "{}:{}".format(host, port)

        # Keep a session
        self.session = requests.Session()

        # Request counter for json-rpc
        self.request_counter = itertools.count()

        # request headers
        self.headers = {
            'user-agent': AGENT,
            'Content-Type': 'application/json'
        }

    def __getattribute__(self,name):
        try:
            return object.__getattribute__(self, name)
        except AttributeError:
            return self.pb_invoke(name)

    def call(self, method, params):
        value = str(next(self.request_counter))
        encoded = json.dumps({
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": value,
        })

        print("json+rpc data: ", encoded)
        r = self.session.post(
            self.uri,
            data=encoded,
            headers=self.headers,
            timeout=3
        )

        try:
           r.raise_for_status()
        except Exception as er:
           raise er

        response = r.content
        
        if is_string(response):
            result = json.loads(bytes_to_str(response))
        if "error" in result:
            raise ValueError(result["error"])
    
        result = result["result"]
        print("json+rpc result: ", result)

        if "code" in result and result["code"]!=0:
            raise ValueError(result["log"])
        return result
   
   
    @property
    def is_connected(self):
        try:
            response = self.status()
        except IOError:
            return False
        else:
            assert(response['node_info'])
            return True
        assert False

    def _send_transaction(self, name, tx):
        print("^^^^^^^^^^^^^^^6sig: ", list(tx.signatures[0]))
        return self.call(name, {"tx": list(tx.SerializeToString())})

    def broadcast_tx_sync(self, tx):
        return self._send_transaction('broadcast_tx_sync', tx)

    def tx_search(self, query: str, prove: bool, page: int, per_page: int):
        req = {
            query: query,
            prove: prove,
            page: page, 
            per_page: per_page,
        }
        return self.call('tx_search', req)

    def abci_query(self, path: str, data: str, height: int=None, prove: bool=False):
        req = RequestQuery(path=path,data=data,height=height,prove=prove)
        return self.pb_invoke("abci_query")(req)

    def abci_info(self):
        return self.pb_invoke("abci_info")(RequestInfo())

    def status(self):
        return self.call('status', [])

    def pb_invoke(self, method_name) -> bytes:
        def wrapper(req: Message):
            payload = json_format.MessageToDict(req)
            print("Payload ",payload)
            print("type(Payload) ",type(payload))
            if method_name == "abci_query":
                payload["data"] = base64.b64decode(payload["data"]).hex()
            result = self.call(method_name, payload)
            print("################ result: ", result)
            return result['response']['value']
        return wrapper
