from typing import Literal
from common.integrations.base import BaseCustomApiSchema


ChatTypes = Literal["private", "group", "supergroup", "channel"]  # https://core.telegram.org/bots/api#chat


class TelegramChat(BaseCustomApiSchema):
    # Docs: https://core.telegram.org/bots/api#chat
    id: int
    type: ChatTypes
    title: str | None = None
