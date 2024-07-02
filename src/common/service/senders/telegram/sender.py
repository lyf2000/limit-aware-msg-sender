from typing import Callable
from common.service.senders.base import BaseSenderService, MessageSendingResult
from common.service.senders.telegram.mixin import SendTextMixin


class TelegramMessageSenderService(SendTextMixin, BaseSenderService):
    """
    Docs:
        https://core.telegram.org/bots/api#available-methods
    """

    async def send(self) -> MessageSendingResult:
        return await self._select_method()()

    def _select_method(self) -> Callable:
        return self.send_text
