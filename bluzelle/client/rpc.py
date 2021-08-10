from base64 import b64decode
from bluzelle.tendermint import Tendermint34Client
from grpc import Channel,UnaryUnaryMultiCallable
from google.protobuf.message import Message

    
class Callable(UnaryUnaryMultiCallable):
    def __init__(self, tendermint34Client: Tendermint34Client, method: str, request_serializer, response_deserializer):
        self.method = method
        self.tendermint34Client = tendermint34Client
        self.request_serializer = request_serializer
        self.response_deserializer = response_deserializer

    def __call__(self, request, timeout, metadata, credentials, wait_for_ready, compression):
        path = self.method[:] # trim `/` chars from start and end of the method.
        value = self.tendermint34Client.abci_query(path, self.request_serializer(request))
        return self.response_deserializer(b64decode(value))
    
    def future(self, request, timeout, metadata, credentials, wait_for_ready, compression):
        return super().future(request, timeout=timeout, metadata=metadata, credentials=credentials, wait_for_ready=wait_for_ready, compression=compression)
    
    def with_call(self, request, timeout, metadata, credentials, wait_for_ready, compression):
        return super().with_call(request, timeout=timeout, metadata=metadata, credentials=credentials, wait_for_ready=wait_for_ready, compression=compression)
    
class RpcChannel(Channel):
    def __init__(self, tendermint34Client: Tendermint34Client):
        self.tendermint34Client = tendermint34Client
    
    def subscribe(self, callback, try_to_connect):
        return super().subscribe(callback, try_to_connect=try_to_connect)
    
    def unsubscribe(self, callback):
        return super().unsubscribe(callback)
    
    def unary_stream(self, method, request_serializer, response_deserializer):
        return super().unary_stream(method, request_serializer=request_serializer, response_deserializer=response_deserializer)
    
    def stream_stream(self, method, request_serializer, response_deserializer):
        return super().stream_stream(method, request_serializer=request_serializer, response_deserializer=response_deserializer)
    
    def stream_unary(self, method, request_serializer, response_deserializer):
        return super().stream_unary(method, request_serializer=request_serializer, response_deserializer=response_deserializer)
    
    def close(self):
        return super().close()

