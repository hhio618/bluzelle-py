from base64 import b64decode
from bluzelle.tendermint import Tendermint34Client
from google.protobuf.message import Message
from .rpc import Callable, RpcChannel

    

class QueryCallable(Callable):
    def __call__(self, request, timeout, metadata, credentials, wait_for_ready, compression):
        path = self.method[:] # trim `/` chars from start and end of the method.
        value = self.tendermint34Client.abci_query(path, self.request_serializer(request))
        return self.response_deserializer(b64decode(value))
    


class QueryClient(RpcChannel):
    def unary_unary(self, method, request_serializer, response_deserializer):
        return QueryCallable(self.tendermint34Client, method, request_serializer, response_deserializer)
