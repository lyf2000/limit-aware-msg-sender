from asyncio import sleep
import logging
from typing import Type
import aiohttp
from abc import ABC, abstractmethod

from common.choices import BaseChoices
from common.client import BaseClient
from common.logic.lock import LimitMessageSendLockService
from common.logic.models.message import MessageEventLogic
from common.service.senders.errors import MessageSendingError, MessageSendingLimitExceedError
from common.service.senders.gateway import SenderServiceGateway
from db.models.message import MessageEvent

logger = logging.getLogger("message.sending")


async def _send(message_event: MessageEvent) -> "MessageSendingResult":
    # TODO what if error -> what to do with locking
    limit_lock = LimitMessageSendLockService(message_event)
    while not await limit_lock.can_send():
        await sleep(0.5)  # TODO

    result = await SenderServiceGateway(message_event).send_message()
    await limit_lock.tried_send()  # TODO check if result OK else not decr
    return result


class MessageSendingResultStatusChoices(BaseChoices):
    SENT = 1
    ERROR = -1
    LIMIT_EXCEEDED = -2

    CHOICES = (
        (SENT, "SENT"),
        (ERROR, "ERROR"),
        (LIMIT_EXCEEDED, "LIMIT_EXCEEDED"),
    )


class MessageSendingResult:
    def __init__(self, message_event: MessageEvent, status: int, detail: None | str = None, code: str | None = None):
        self.message_event = message_event
        self.status = status
        self.detail = detail
        self.code = code

    async def handle(self):
        try:
            await MessageEventLogic.save_sending_result(self)
        finally:
            if self.status == MessageSendingResultStatusChoices.SENT:
                logger.info(f"Sent message {self.message_event.id}")
            elif self.status == MessageSendingResultStatusChoices.LIMIT_EXCEEDED:
                logger.warn(
                    f"Limit exceeded sending message {self.message_event.client.platform}({self.message_event.client.platform_id}), {self.message_event.id}"
                )
                raise MessageSendingLimitExceedError
            elif self.status == MessageSendingResultStatusChoices.ERROR:
                logger.error(
                    f"Error sending message {self.message_event.client.platform}({self.message_event.client.platform_id}), {self.message_event.id}"
                )
                raise MessageSendingError
            else:
                raise ValueError(
                    f"Unexpected result status({self.status}) sending message({self.message_event.id}) detail: {self.detail}"
                )


class IBaseMessageSendMixin:
    client: Type[BaseClient]
    message_event: MessageEvent


class BaseSenderService(ABC):
    def __init__(self, message_event: MessageEvent, client: Type[BaseClient]):
        self.message_event = message_event
        self.client = client

    @abstractmethod
    async def send(self) -> MessageSendingResult:
        pass
