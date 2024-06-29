from contextlib import asynccontextmanager
from functools import partial
from typing import Any, Literal
import aiohttp


METHODS = Literal["get", "post", "put", "delete"]


class BaseClient:
    HEADERS = {}

    async def get(self, url: str, data: dict) -> aiohttp.ClientRequest: ...
    async def post(self, url: str, data: dict) -> aiohttp.ClientRequest: ...
    async def put(self, url: str, data: dict) -> aiohttp.ClientRequest: ...
    async def delete(self, url: str, data: dict) -> aiohttp.ClientRequest: ...

    async def _method(self, method: METHODS, url: str, data: dict) -> aiohttp.ClientRequest:
        async with self._session_context() as session:
            async with getattr(session, method)(url, data=data) as response:
                # async with session.post(url, data=data) as response:
                await response.read()
            return response

    @asynccontextmanager
    async def _session_context(self) -> aiohttp.ClientSession:
        async with aiohttp.ClientSession(headers=self.HEADERS) as session:
            yield session

    def __getattribute__(self, name: str) -> Any:
        if name in ("get", "post", "put", "delete"):
            return partial(self._method, method=name)
        return super().__getattribute__(name)
