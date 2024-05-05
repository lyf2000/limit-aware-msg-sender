from typing import Type

from sqlalchemy import select

from db.connection import get, get_session, get_session_context
from db.models.base import Base


class BaseModelService:
    MODEL: Type[Base]

    @classmethod
    async def create(cls, obj: "MODEL"):
        with get_session_context() as session:
            session.add(obj)
            session.commit()

    @classmethod
    async def get(cls, **kwargs):
        return await get(cls.select_by(**kwargs))

    @classmethod
    def select_by(cls, **kwargs):
        return select(cls.MODEL).filter(**kwargs)
