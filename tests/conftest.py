import os
import sys
from unittest.mock import AsyncMock, patch

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(PROJECT_PATH, "src")
sys.path.append(SOURCE_PATH)


import pytest

from sqlalchemy.ext.asyncio import AsyncSession
from db.models.base import a_engine_factory, Base, engine_factory as engine_
from tests.fixtures import *
from functools import partial


apatch = partial(patch, new_callable=AsyncMock)


@pytest.fixture()
def settings():
    from common.settings import settings

    return settings


@pytest.fixture(scope="session")
async def aengine():
    yield a_engine_factory()
    # a_engine.sync_engine.dispose()


@pytest.fixture(scope="session")
async def engine():
    yield engine_()
    # engine_.dispose()


@pytest.fixture()
async def session(aengine):
    async with AsyncSession(aengine) as session:
        yield session
        # await session_.rollback()


@pytest.fixture(autouse=True)
def setup_database(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
