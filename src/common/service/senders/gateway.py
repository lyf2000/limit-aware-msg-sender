from typing import Type
from common.client import BaseClient
from common.service.senders.base import BaseSenderService, MessageSendResult
from common.service.senders.telegram.client import TelegramClient
from common.service.senders.telegram.sender import TelegramMessageSenderService
from common.service.senders.vk import VkMessageSenderService
from db.models.message import MessageEvent
from db.models.platform import PlatformTypeChoices


class SenderServiceGateway:
    def __init__(self, message_event: MessageEvent):
        self.message_event = message_event
        self.client = self._client_factory()
        self.sender = self._sender_factory()

    def _client_factory(self) -> BaseClient | Type[BaseClient]:
        return {
            PlatformTypeChoices.TELEGRAM: TelegramClient,
        }.get(self.message_event.client.platform.type, BaseClient)()

    def _sender_factory(self) -> Type[BaseSenderService]:
        sender_service = {
            PlatformTypeChoices.TELEGRAM: TelegramMessageSenderService,
            PlatformTypeChoices.VK: VkMessageSenderService,
        }[self.message_event.client.platform.type]

        return sender_service(
            message_event=self.message_event,
            client=self.client,
        )

    async def send_message(self) -> MessageSendResult:
        return await self.sender.send()
