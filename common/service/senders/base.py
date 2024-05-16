from typing import Type
import aiohttp
from abc import ABC, abstractmethod

from common.client import BaseClient
from db.models.message import MessageEvent


class MessageSendResultStatusChoices:
    SENT = 1
    ERROR = -1
    LIMIT_EXCEEDED = -2


class MessageSendResult:
    def __init__(self, status: int, detail: None | str = None, code: str | None = None):
        self.status = status
        self.detail = detail
        self.code = code


class IBaseMessageSendMixin:
    client: Type[BaseClient]
    message_event: MessageEvent


class BaseSenderService(ABC):
    def __init__(self, message_event: MessageEvent, client: Type[BaseClient]):
        self.message_event = message_event
        self.client = client

    @abstractmethod
    async def send(self) -> MessageSendResult:
        pass
