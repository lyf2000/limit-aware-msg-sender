from contextlib import nullcontext
from typing import Type

from sqlalchemy import select as db_select

from db.connection import get as db_get, get_session_context, list as db_list
from db.models.base import Base
from sqlalchemy.ext.asyncio import AsyncSession


class BaseModelService[T: Type[Base]]:
    MODEL: T

    list = db_list
    get = db_get
    select = db_select

    @classmethod
    async def create(cls, obj: "MODEL", session_: AsyncSession | None = None):
        async with nullcontext() if session_ else get_session_context() as session:
            if session_:
                session = session_

            session.add(obj)
            await session.commit()
