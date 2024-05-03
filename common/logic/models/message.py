from db.models.message import MessageEvent


class MessageEventLogic:
    @classmethod
    async def message_sent_success(cls, message_event: MessageEvent): ...
