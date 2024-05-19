from abc import ABC, abstractmethod
import ast
import asyncio
from functools import wraps
import json
from typing import Callable


def bytes_to_dict(string: bytes) -> dict:
    return json.loads(string)


class BaseDecorator(ABC):
    def __call__(self, function: Callable):
        @wraps(function)
        async def wrapper(*args, **kwargs):

            return await self._call(
                (
                    await function(*args, **kwargs)
                    if asyncio.iscoroutinefunction(function)
                    else function(*args, **kwargs)
                )
            )

        return wrapper

    @abstractmethod
    async def _call(self, *args, **kwargs): ...


def asyncinit(cls):
    async def init(obj, *arg, **kwarg):
        await obj.__init__(*arg, **kwarg)
        return obj

    def new(cls, *arg, **kwarg):
        obj = object().__new__(cls)
        coro = init(obj, *arg, **kwarg)
        return coro

    cls.__new__ = new
    return cls
