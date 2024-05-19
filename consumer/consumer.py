import logging

from common.logic.lock import LimitMessageSendLockService
from asyncio import sleep
from common.logic.models.message import MessageEventLogic
from common.service.senders.base import MessageSendResult, MessageSendResultStatusChoices
from common.service.senders.errors import MessageSendError, MessageSendLimitExceedError
from common.service.senders.gateway import SenderServiceGateway
from consumer.schema import ConsumerMessage
from db.connection import get, get_session_context
from db.models.client import Client
from db.models.message import MessageEvent
from db.models.platform import Platform
from db.service.message import MessageModelService


logger = logging.getLogger("message.sending")


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

        await _handle_send_result(result, message_event)


async def _send(message_event: MessageEvent) -> MessageSendResult:
    # TODO what if error -> what to do with locking
    limit_lock = LimitMessageSendLockService(message_event)
    while not await limit_lock.can_send():
        await sleep(0.5)  # TODO

    result = await SenderServiceGateway(message_event).send_message()
    await limit_lock.tried_send()  # TODO check if result OK else not decr
    return result


async def _handle_send_result(result: MessageSendResult, message_event: MessageEvent):
    await MessageEventLogic.message_sending_event(message_event, result)

    if result.status == MessageSendResultStatusChoices.SENT:
        logger.info(f"Sent message {message_event.id}")
    elif result.status == MessageSendResultStatusChoices.LIMIT_EXCEEDED:
        logger.warn(
            f"Limit exceeded sending message {message_event.client.platform}({message_event.client.platform_id}), {message_event.id}"
        )
        raise MessageSendLimitExceedError
    elif result.status == MessageSendResultStatusChoices.ERROR:
        logger.error(
            f"Error sending message {message_event.client.platform}({message_event.client.platform_id}), {message_event.id}"
        )
        raise MessageSendError
    else:
        raise ValueError(
            f"Unexpected result status({result.status}) sending message({message_event.id}) detail: {result.detail}"
        )
