from common.integrations.telegram.api import TelegramApiClient
from common.integrations.telegram.schema import ChatTypes as TgChatTypes
from db.models.message import MessageEvent
from db.models.platform import PlatformTypeChoices


class PlatformIntegrationGateway:
    def __init__(self, message_event: MessageEvent) -> None:
        self.message_event = message_event

    async def get_chat_type(self) -> TgChatTypes:
        if self.message_event.client.platform.type == PlatformTypeChoices.TELEGRAM:
            return (
                await TelegramApiClient(self.message_event.client.token).get_chat_info(
                    chat_id=self.message_event.chat_id
                )
            ).type

        raise NotImplementedError(
            f"Not found type({self.message_event.client.platform.type}) for message event({self.message_event.id})"
        )
