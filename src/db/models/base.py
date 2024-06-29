from sqlalchemy import UUID, Column, Integer, MetaData, create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from common.settings import settings


a_engine = create_async_engine(settings.APOSTGRES_URL, echo=True, future=True)
engine = create_engine(settings.POSTGRES_URL, echo=True, future=True)


class Base(DeclarativeBase):
    pass


convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

Base.metadata = MetaData(naming_convention=convention)


class BaseModel(Base):
    __abstract__ = True
    id = Column(Integer(), primary_key=True)


class UUIDBaseModel(Base):
    __abstract__ = True
    id = Column(UUID(), primary_key=True)
