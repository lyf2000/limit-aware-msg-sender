from abc import ABC, abstractmethod
from typing import Any, Protocol, cast
from cache.redis.conneciton import get_session
from common.utils import asyncinit


CacheValue = Any


class CacheApiProtocol(Protocol):
    TIMEOUT: int

    async def get(self, *args, **kwargs): ...
    async def set(self, *args, **kwargs): ...
    async def _get(self, key: str): ...
    async def _set(self, key: str, val: CacheValue): ...
    async def _parse_to_value(self, value: CacheValue) -> Any: ...


@asyncinit
class BaseRedisApi(CacheApiProtocol, ABC):
    TIMEOUT = 604800  # 7 days

    async def __init__(self) -> None:
        self._cache = await get_session()

    @abstractmethod
    async def get(self, *args, **kwargs): ...

    @abstractmethod
    async def set(self, *args, **kwargs): ...

    async def exp(self) -> int:
        return self.TIMEOUT

    async def _get(self, key: str):
        return await self._cache.get(key)

    async def _set(self, key: str, val: CacheValue, exp: int | None = None):
        return await self._cache.set(key, val, ex=exp or await self.exp())


class CacheClientProtocol(CacheApiProtocol):
    TIMEOUT: int

    async def _get_key(self) -> str: ...


class InitValueCacheMixin(CacheClientProtocol):
    @abstractmethod
    async def _init_value_to_cache(self) -> CacheValue: ...

    async def set_init(self):
        return await self._set(
            await self._get_key(),
            await self._init_value_to_cache(),
        )

    async def get(self):
        if (result := await self._get(await self._get_key())) is None:  # type: ignore
            await self.set_init()
            return await super().get()
        return await self._parse_to_value(result)


class BaseDetailRedisClient(CacheClientProtocol, BaseRedisApi):
    @abstractmethod
    async def _get_key(self) -> str: ...

    async def _parse_to_cache(self, value: Any) -> CacheValue:
        value = cast(CacheValue, value)
        return value

    async def _parse_to_value(self, value: CacheValue) -> Any:
        return value

    async def get(self):
        return await self._parse_to_value(await self._get(await self._get_key()))

    async def set(self, value: Any | None = None):
        return await self._set(
            await self._get_key(),
            (value if value is not None else await self._parse_to_cache(value)),
        )
