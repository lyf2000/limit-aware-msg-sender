from common.service.senders.base import BaseSenderService, MessageSendResult


class VkMessageSenderService(BaseSenderService):
    def send(self) -> MessageSendResult: ...
