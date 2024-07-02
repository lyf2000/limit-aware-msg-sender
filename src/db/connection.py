from contextlib import asynccontextmanager, nullcontext
import logging
from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.base import a_engine_factory


logger = logging.getLogger("db.session")


@asynccontextmanager
async def get_session_context() -> AsyncSession:
    logger.info("session created")
    async_session = sessionmaker(a_engine_factory(), class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def get_session() -> AsyncSession:
    async with get_session_context() as session:
        yield session


async def list(q, session_=None):
    async with nullcontext() if session_ else get_session_context() as session:
        session = session_ if session_ else session
        return (await session.execute(q)).scalars().all()


async def get(q, session_=None):
    return (await list(q, session_))[0]


async def count(q, session_=None):
    async with nullcontext() if session_ else get_session_context() as session:
        count_q = q.with_only_columns(func.count()).order_by(None).select_from(q.get_final_froms()[0])
        iterator = await session.execute(count_q)
        print(iterator)
        for count in iterator:
            return count[0]
        return 0
