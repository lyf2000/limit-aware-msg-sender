from abc import ABC, abstractmethod
from typing import Type, cast, override
from common.service.senders.base import (
    IBaseMessageSendMixin,
    MessageSendResult,
    MessageSendResultStatusChoices,
)
from common.service.senders.telegram.schema import BaseTelegramMessageSchema, SendTextMessageSchema
from common.utils import bytes_to_dict


class BaseTelegramSendMessageMixin[T: Type[BaseTelegramMessageSchema]](ABC, IBaseMessageSendMixin):
    METHOD_NAME: str

    @abstractmethod
    def _get_schema_data(self, **kwargs) -> T: ...

    def _get_url(self) -> str:
        return f"https://api.telegram.org/bot{self.message_event.client.token}/{self.METHOD_NAME}"

    async def _send(self) -> MessageSendResult:
        url = self._get_url()
        data = self._get_schema_data()

        response = await self.client.post(url=url, data=data.model_dump_json(exclude_none=True))  # TODO fix hint

        if response.ok:
            return MessageSendResult(MessageSendResultStatusChoices.SENT)

        err = bytes_to_dict(response._body)
        return MessageSendResult(
            status=MessageSendResultStatusChoices.ERROR,
            detail=err["description"],
            code=err["error_code"],
        )


class SendTextMixin(BaseTelegramSendMessageMixin):
    """
    Docs:
        https://core.telegram.org/method/messages.sendMessage
    """

    METHOD_NAME = "sendMessage"

    async def send_text(self) -> MessageSendResult:
        return await self._send()

    @override
    def _get_schema_data(self) -> SendTextMessageSchema:
        return SendTextMessageSchema(
            chat_id=self.message_event.chat_id,
            text=self.message_event.text,
            reply_to=self.message_event.reply_to,
        )
