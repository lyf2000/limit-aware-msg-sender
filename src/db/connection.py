from contextlib import asynccontextmanager, nullcontext
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.base import a_engine


@asynccontextmanager
async def get_session_context() -> AsyncSession:
    async_session = sessionmaker(a_engine, class_=AsyncSession, expire_on_commit=False)
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
