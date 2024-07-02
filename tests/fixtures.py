import random
import pytest
import string as string_

from common.choices import BaseChoices
from db.models.client import Client
from db.models.message import MessageEvent, MessageStatusChoices
from db.models.platform import Platform, PlatformTypeChoices
from db.service.client import ClientModelService
from db.service.message import MessageModelService
from db.service.platform import PlatformModelService


@pytest.fixture(scope="session")
def rand_choice():
    def make(klass: type[BaseChoices]):
        return random.choice(list(klass.keys()))

    return make


@pytest.fixture(scope="session")
def string(len_=12):
    def make():
        return "".join(random.choice(string_.ascii_uppercase + string_.digits) for _ in range(len_))

    return make


@pytest.fixture(scope="session")
def number(left: int = -10000, right: int = 10000):
    def make():
        return random.randint(left, right)

    return make


# region models


@pytest.fixture()
async def platform(string, rand_choice):
    async def make():
        return await PlatformModelService.create(
            Platform(
                name=string(),
                type=rand_choice(PlatformTypeChoices),
            )
        )

    return make


@pytest.fixture()
async def platform_(platform):
    return await platform()


@pytest.fixture()
async def client(string, platform_):
    async def make():
        return await ClientModelService.create(
            Client(
                name=string(),
                token=string(),
                platform_id=platform_.id,
            )
        )

    return make


@pytest.fixture()
async def client_(client):
    return await client()


@pytest.fixture()
async def message_event(string, rand_choice, client_):
    async def make():
        return await MessageModelService.create(
            MessageEvent(
                text=string(),
                chat_id=string(),
                reply_to=string(),
                status=rand_choice(MessageStatusChoices),
                client_id=client_.id,
            )
        )

    return make


@pytest.fixture()
async def message_event_(message_event):
    return await message_event()


# endregion models
