from common.service.senders.base import BaseSenderService, MessageSendingResult


class VkMessageSenderService(BaseSenderService):
    def send(self) -> MessageSendingResult: ...
