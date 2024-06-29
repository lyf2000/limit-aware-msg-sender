from contextlib import asynccontextmanager
from functools import partial, wraps
from typing import Any, Callable, Literal
import aiohttp

from common.schema import CustomBaseModel
from common.utils import BaseDecorator, bytes_to_dict


METHODS = Literal["get", "post", "put", "delete"]


# schema


class BaseCustomApiSchema(CustomBaseModel):
    pass


# requset


class SchemaResponseBodyDecorator[T: type[BaseCustomApiSchema]](BaseDecorator):
    def __init__(self, schema: T) -> None:
        self.schema = schema

    async def _call(self, body: dict) -> T:
        return self.schema(**(bytes_to_dict(body._body))["result"])  # TODO


class BaseApiClient:
    HEADERS = {}

    async def get(self, url: str, data: dict | None = None) -> aiohttp.ClientRequest: ...
    async def post(self, url: str, data: dict | None = None) -> aiohttp.ClientRequest: ...
    async def put(
        self,
        url: str,
    ) -> aiohttp.ClientRequest: ...
    async def delete(self, url: str) -> aiohttp.ClientRequest: ...

    async def _method(self, method: METHODS, url: str, data: dict | None = None) -> aiohttp.ClientRequest:
        data = data or {}
        async with self._session_context() as session:
            async with getattr(session, method)(url, data=data) as response:
                await response.read()
            return response

    @asynccontextmanager
    async def _session_context(self) -> aiohttp.ClientSession:
        async with aiohttp.ClientSession(**(await self.session_kwargs())) as session:
            yield session

    async def session_kwargs(self) -> dict:
        return dict(
            headers=await self.headers(),
        )

    async def headers(self):
        return self.HEADERS

    def __getattribute__(self, name: str) -> Any:
        if name in ("get", "post", "put", "delete"):
            return partial(self._method, method=name)
        return super().__getattribute__(name)
