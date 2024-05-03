from alembic import context
from sqlalchemy import create_engine

from common.db.models.base import Base
from common.db.models.client import Client
from common.db.models.message import MessageEvent
from common.db.models.platform import Platform
from common.db.models.conversation import ConversationType, ConversationRule

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
