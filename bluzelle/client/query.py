from base64 import b64decode
import logging
from typing import Any

from .rpc import Callable, RpcChannel


class QueryCallable(Callable):
    async def _blocking(
        self, request, timeout, metadata, credentials, wait_for_ready, compression
    ) -> Any:
        """request's path will be derived from its info, and an abci_query will
        be.

        sent using derived path and request's value.
        """
        path = self.method[:]
        value = await self.tendermint34Client.abci_query(path, self.request_serializer(request))
        return self.response_deserializer(b64decode(value))


class QueryClient(RpcChannel):
    """QueryClient acts as a bridge between custom protobuf Message type.

    query requests and Tendermint34Client.abci_query.
    """

    def __init__(self, tendermint34Client, logging_level: int = logging.INFO):
        super().__init__(tendermint34Client)
        self.logging_level = logging_level

    def unary_unary(self, method, request_serializer, response_deserializer) -> Any:
        """Custom implementation of grpc Channel that uses tendermint client
        as.

        it's transport.
        """
        return QueryCallable(
            self.tendermint34Client, method, request_serializer, response_deserializer
        )
