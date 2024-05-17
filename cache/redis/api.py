from abc import ABC, abstractmethod
from typing import Any
from cache.redis.conneciton import get_session
from common.utils import asyncinit


CacheValue = Any


@asyncinit
class BaseRedisApi(ABC):
    TIMEOUT = 604800  # 7 days

    async def __init__(self) -> None:
        self._cache = await get_session()

    @abstractmethod
    async def get(self, *args, **kwargs): ...

    @abstractmethod
    async def set(self, *args, **kwargs): ...

    async def _get(self, key: str):
        return await self._cache.get(key)

    async def _set(self, key: str, val: CacheValue):
        return await self._cache.set(key, val, ex=self.TIMEOUT)


class BaseDetailRedisApi(BaseRedisApi):
    @abstractmethod
    async def _get_key(self) -> str: ...

    @abstractmethod
    async def _value_to_cache(self) -> CacheValue: ...

    async def _cache_to_value(self, value: CacheValue) -> Any:
        return value

    async def get(self):
        return await self._cache_to_value(await self._get(await self._get_key()))

    async def set(self):
        return await self._set(
            await self._get_key(),
            await self._value_to_cache(),
        )
