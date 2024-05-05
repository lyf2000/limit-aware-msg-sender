import logging
from common.logic.lock import LimitLockService
from asyncio import sleep
from common.logic.models.message import MessageEventLogic
from common.service.senders import MESSAGE_SERVICE_PLATFORM_TYPE_MAP
from common.service.senders.base import MessageSendResult, MessageSendResultStatusChoices
from common.service.senders.errors import MessageSendError, MessageSendLimitExceedError
from consumer.schema import ConsumerMessage
from db.models.message import MessageEvent
from db.service.message import MessageModelService


logger = logging.getLogger("message.sending")


# TODO add logging decorator
async def consume(message: ConsumerMessage):
    message_event = MessageEvent(
        text=message.text,
        client_id=message.client_id,
        type=message.type,
    )
    await MessageModelService.create(message_event)

    logger.info(f"Sending {message_event.id}")
    result = await _send(message_event)

    await _handle_send_result(result, message_event)


async def _send(message_event: MessageEvent):
    # TODO what if error -> what to do with locking
    while not await LimitLockService(message_event).can_send():
        await sleep(0.5)  # TODO
    return await MESSAGE_SERVICE_PLATFORM_TYPE_MAP[message_event.client.platform.type](message_event).send()


async def _handle_send_result(result: MessageSendResult, message_event: MessageEvent):

    if result.status == MessageSendResultStatusChoices.SENT:
        logger.info(f"Sent message {message_event.id}")
        await MessageEventLogic.message_sent_success(message_event)
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
