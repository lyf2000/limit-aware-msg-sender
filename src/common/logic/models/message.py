from typing import TYPE_CHECKING
from sqlalchemy.ext.asyncio import AsyncSession
from db.service.message import MessageModelService


if TYPE_CHECKING:
    from common.service.senders.base import MessageSendingResult


class MessageEventLogic:
    @classmethod
    async def save_sending_result(cls, result: "MessageSendingResult", session: AsyncSession | None = None):
        result.message_event.status = result.status
        await MessageModelService.save(result.message_event, session)
