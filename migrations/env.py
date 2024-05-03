from alembic import context
from sqlalchemy import create_engine

from db.models.base import Base
from db.models.client import Client
from db.models.message import MessageEvent
from db.models.platform import Platform
from db.models.conversation import ConversationType, ConversationRule

from common.settings import settings


config = context.config


def run_migrations_online() -> None:
    engine = create_engine(settings.POSTGRES_URL)
    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=Base.metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
