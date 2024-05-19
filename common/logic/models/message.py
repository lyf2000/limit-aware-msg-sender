from sqlalchemy.ext.asyncio import AsyncSession
from common.service.senders.base import MessageSendResult
from db.models.message import MessageEvent, MessageStatusChoices
from db.service.message import MessageModelService


class MessageEventLogic:
    @classmethod
    async def message_sending_event(
        cls, message_event: MessageEvent, result: MessageSendResult, session: AsyncSession | None = None
    ):
        message_event.status = result.status
        await MessageModelService.save(message_event, session)
