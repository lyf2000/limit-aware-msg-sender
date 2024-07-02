import pytest
from common.service.senders.base import MessageSendingResultStatusChoices, MessageSendingResult, _send
from common.service.senders.errors import MessageSendingError, MessageSendingLimitExceedError
from consumer.consume import consume
from consumer.schema import ConsumerMessage
from unittest.mock import patch
from db.models.client import Client
from db.models.platform import Platform
from tests.conftest import apatch
from unittest.mock import call
from db.service.message import MessageModelService


@patch("common.service.senders.base.MessageSendingResult.handle")
@apatch("consumer.consume._send")
async def test_consume(mocked_send, mocked_handle_send_result, string, client_):
    # GIVEN
    mocked_send.return_value = MessageSendingResult
    message = ConsumerMessage(
        client_id=client_.id,
        text=string(),
        chat_id=string(),
    )

    # WHEN
    assert await MessageModelService.count() == 0
    await consume(message)

    # THEN
    assert await MessageModelService.count() == 1
    mocked_send.assert_called_once_with(await MessageModelService.get())
    mocked_handle_send_result.assert_called_once()


@pytest.mark.skip
@apatch("consumer.consume._send")
async def test_consume_joins_passed(mocked_send, string, client_, subtests):
    # GIVEN
    mocked_send.return_value = MessageSendingResult
    message = ConsumerMessage(
        client_id=client_.id,
        text=string(),
        chat_id=string(),
    )

    # WHEN THEN
    with patch("common.service.senders.base.MessageSendingResult.handle"):
        await consume(message)
    for status in MessageSendingResultStatusChoices.keys():
        with patch("common.service.senders.base.MessageEventLogic.save_sending_result"):
            with subtests.test():
                await MessageSendingResult(
                    message_event=mocked_send.call_args[0][0],
                    status=status,
                    detail=string(),
                    code=string(),
                ).handle()


# region send


@apatch("consumer.consume.SenderServiceGateway.send_message")
@patch("consumer.consume.SenderServiceGateway.__init__", return_value=None)
@apatch("consumer.consume.LimitMessageSendLockService.can_send")
@apatch("consumer.consume.LimitMessageSendLockService.tried_send")
async def test_send(mocked_tried_send, mocked_can_send, m, mocked_send_message, message_event_):
    # GIVEN
    mocked_can_send.return_value = True
    mocked_send_message.return_value = object()

    # WHEN
    result = await _send(message_event_)

    # THEN
    mocked_can_send.assert_called_once()
    mocked_tried_send.assert_called_once()
    assert result == mocked_send_message.return_value


@apatch("common.service.senders.base.sleep")
@apatch("consumer.consume.SenderServiceGateway.send_message")
@patch("consumer.consume.SenderServiceGateway.__init__", return_value=None)
@apatch("consumer.consume.LimitMessageSendLockService.can_send")
@apatch("consumer.consume.LimitMessageSendLockService.tried_send")
async def test_send_can_send_after_sleep(
    mocked_tried_send, mocked_can_send, m, mocked_send_message, mocked_sleep, message_event_
):
    # GIVEN
    mocked_can_send.side_effect = (False, True)
    mocked_send_message.return_value = object()

    # WHEN
    result = await _send(message_event_)

    # THEN
    mocked_can_send.assert_has_calls((call(), call()))
    mocked_sleep.assert_called_once_with(0.5)
    mocked_tried_send.assert_called_once()
    assert result == mocked_send_message.return_value


# endregion send


# region handle_send_result


@patch("common.service.senders.base.MessageEventLogic.save_sending_result")
@pytest.mark.parametrize(
    "status,error",
    (
        (MessageSendingResultStatusChoices.SENT, None),
        (MessageSendingResultStatusChoices.LIMIT_EXCEEDED, MessageSendingLimitExceedError),
        (MessageSendingResultStatusChoices.ERROR, MessageSendingError),
        ("b", ValueError),
    ),
)
async def test_handle_send_result(mocked_save_sending_result, status, error, string, message_event_):
    # GIVEN
    message_event_ = await MessageModelService.get()
    result = MessageSendingResult(
        message_event=message_event_,
        status=status,
        detail=string(),
        code=string(),
    )

    # WHEN THEN
    if error:
        with pytest.raises(error):
            await result.handle()
    else:
        await result.handle()

    mocked_save_sending_result.assert_called_once_with(result)


# endregion handle_send_result
