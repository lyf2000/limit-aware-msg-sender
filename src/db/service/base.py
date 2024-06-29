from contextlib import nullcontext
from typing import Type

from sqlalchemy import select as db_select

from db.connection import get as db_get, get_session_context, list as db_list
from db.models.base import Base
from sqlalchemy.ext.asyncio import AsyncSession


class BaseModelService[T: Type[Base]]:
    MODEL: T

    @classmethod
    def select(cls):
        return db_select(cls.MODEL)

    @classmethod
    async def create(cls, obj: T, session_: AsyncSession | None = None):
        async with nullcontext() if session_ else get_session_context() as session:
            if session_:
                session = session_

            session.add(obj)
            await session.commit()

    @classmethod
    async def save(cls, obj: T, session_: AsyncSession | None = None):  # TODO fix
        async with nullcontext() if session_ else get_session_context() as session:
            obj_ = await cls.get(cls.select().where(cls.MODEL.id == obj.id), session=session)
            for column in cls.MODEL.__table__.columns:
                setattr(obj_, column.key, getattr(obj, column.key))

            await session.commit()

    @classmethod
    async def get(cls, q, session: AsyncSession | None = None):
        return await db_get(q, session)

    @classmethod
    async def list(cls, q, session: AsyncSession | None = None):
        return await db_list(q, session)
