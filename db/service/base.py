from contextlib import nullcontext
from typing import Type

from sqlalchemy import select

from db.connection import get, get_session_context
from db.models.base import Base
from sqlalchemy.ext.asyncio import AsyncSession


class BaseModelService:
    MODEL: Type[Base]

    @classmethod
    async def create(cls, obj: "MODEL", session_: AsyncSession | None = None):
        async with nullcontext() if session_ else get_session_context() as session:
            if session_:
                session = session_

            session.add(obj)
            await session.commit()

    @classmethod
    async def get(cls, **kwargs):
        return await get(cls.select_by(**kwargs))

    @classmethod
    def select_by(cls, **kwargs):
        return select(cls.MODEL).filter(**kwargs)
