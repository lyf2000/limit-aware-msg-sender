import os
import sys

PROJECT_PATH = os.getcwd()
SOURCE_PATH = os.path.join(PROJECT_PATH, "src")
sys.path.append(SOURCE_PATH)


import pytest
from alembic.config import Config
from alembic import command

from db.connection import get_session_context
from db.models.base import a_engine, Base


@pytest.fixture()
def settings():
    from common.settings import settings

    return settings


@pytest.fixture(scope="session")
async def engine():
    return a_engine


@pytest.fixture(scope="session")
async def session():
    async with get_session_context() as session_:
        yield session_
        await session_.rollback()


def drop_db(engine):
    try:
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
    except Exception as e:
        print(e)


# TODO disable for unused cases
@pytest.fixture(autouse=True)
def setup_database(engine):
    drop_db(engine)

    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")  # Upgrade to the latest migration

    drop_db(engine)
