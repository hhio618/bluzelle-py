import abc

from grpc import Channel, UnaryUnaryMultiCallable

from bluzelle.tendermint import Tendermint34Client


class Callable(UnaryUnaryMultiCallable):
    def __init__(
        self,
        tendermint34Client: Tendermint34Client,
        method: str,
        request_serializer,
        response_deserializer,
    ):
        """Custom implementation of grpc UnaryUnaryMultiCallable object using
        Tendermint34Client.

        Args:
          tendermint34Client: A Tendermint34Client instance.
          method: The grpc Service method name.
          request_serializer: Protobuf Message serializer.
          response_deserializer: Protobuf Message deserializer.
        """
        self.method = method
        self.tendermint34Client = tendermint34Client
        self.request_serializer = request_serializer
        self.response_deserializer = response_deserializer

    def __call__(self, request, timeout, metadata, credentials, wait_for_ready, compression):
        return self._blocking(request, timeout, metadata, credentials, wait_for_ready, compression)

    @abc.abstractmethod
    def _blocking(self, request, timeout, metadata, credentials, wait_for_ready, compression):
        """Handles invokes the underlying RPC synchronously."""
        raise NotImplementedError()

    def future(self, request, timeout, metadata, credentials, wait_for_ready, compression):
        return super().future(
            request,
            timeout=timeout,
            metadata=metadata,
            credentials=credentials,
            wait_for_ready=wait_for_ready,
            compression=compression,
        )

    def with_call(self, request, timeout, metadata, credentials, wait_for_ready, compression):
        return super().with_call(
            request,
            timeout=timeout,
            metadata=metadata,
            credentials=credentials,
            wait_for_ready=wait_for_ready,
            compression=compression,
        )


class RpcChannel(Channel):
    """Base class for implementing A GRPC Channel using Tendermint34Client."""

    def __init__(self, tendermint34Client: Tendermint34Client):
        self.tendermint34Client = tendermint34Client

    def subscribe(self, callback, try_to_connect):
        return super().subscribe(callback, try_to_connect=try_to_connect)

    def unsubscribe(self, callback):
        return super().unsubscribe(callback)

    def unary_stream(self, method, request_serializer, response_deserializer):
        return super().unary_stream(
            method,
            request_serializer=request_serializer,
            response_deserializer=response_deserializer,
        )

    def stream_stream(self, method, request_serializer, response_deserializer):
        return super().stream_stream(
            method,
            request_serializer=request_serializer,
            response_deserializer=response_deserializer,
        )

    def stream_unary(self, method, request_serializer, response_deserializer):
        return super().stream_unary(
            method,
            request_serializer=request_serializer,
            response_deserializer=response_deserializer,
        )

    def close(self):
        return super().close()
