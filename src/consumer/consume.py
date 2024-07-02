import logging

from common.logic.lock import LimitMessageSendLockService
from asyncio import sleep
from common.service.senders.base import MessageSendingResult, _send
from common.service.senders.gateway import SenderServiceGateway
from consumer.schema import ConsumerMessage
from db.connection import get_session_context
from db.models.client import Client
from db.models.message import MessageEvent
from db.models.platform import Platform
from db.service.message import MessageModelService


logger = logging.getLogger(__name__)


# TODO add logging decorator
async def consume(message: ConsumerMessage):
    async with get_session_context() as session:
        message_event = MessageEvent(
            text=message.text,
            chat_id=message.chat_id,
            client_id=message.client_id,
            # type=message.type,
        )
        await MessageModelService.create(message_event, session)

        q = MessageModelService.select().where(MessageEvent.id == message_event.id).join(Client).join(Platform)
        message_event = await MessageModelService.get(q)
        logger.info(f"Sending {message_event.id}")
        result = await _send(message_event)

        await result.handle()
