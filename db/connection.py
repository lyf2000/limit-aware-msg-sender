from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession

from db.models.base import engine


@asynccontextmanager
async def get_session_context() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
        await session.close()


async def get_session() -> AsyncSession:
    async with get_session_context() as session:
        yield session


async def get(q):
    return (await get_session()).execute(q).one()