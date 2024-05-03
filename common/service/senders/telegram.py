from common.service.senders.base import BaseSenderService, MessageSendResult


class TelegramMessageSenderService(BaseSenderService):
    def send(self) -> MessageSendResult: ...
