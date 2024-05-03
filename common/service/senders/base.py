from abc import ABC, abstractmethod

from db.models.message import MessageEvent


class MessageSendResultStatusChoices:
    SENT = 1
    ERROR = -1
    LIMIT_EXCEEDED = -2


class MessageSendResult:
    def __init__(self, status: int, detail: None | str = None):
        self.status = status
        self.detail = detail


class BaseSenderService(ABC):
    def __init__(self, message_event: MessageEvent):
        self.message_event = message_event

    @abstractmethod
    async def send(self) -> MessageSendResult:
        pass
