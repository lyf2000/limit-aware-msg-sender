from db.models.message import MessageEvent
from db.service.base import BaseModelService


class MessageModelService(BaseModelService):
    MODEL = MessageEvent

    @classmethod
    def get_chat_type(cls, message_event: MessageEvent) -> str: ...
