from typing import TYPE_CHECKING
from sqlalchemy import String, SmallInteger
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy_utils import ChoiceType

from db.models.base import BaseModel


if TYPE_CHECKING:
    from db.models.conversation import ConversationType
    from db.models.message import MessageEvent
    from db.models.client import Client


class PlatformTypeChoices:
    TELEGRAM = 1
    VK = 2

    CHOICES = (
        (TELEGRAM, "telegram"),
        (VK, "vk"),
    )


class Platform(BaseModel):
    __tablename__ = "platforms"

    name = mapped_column(String(64), nullable=False)
    type = mapped_column(ChoiceType(PlatformTypeChoices.CHOICES, impl=SmallInteger), nullable=False)  # TODO unique?

    conversation_types: Mapped[list["ConversationType"]] = relationship("ConversationType")
    message_events: Mapped[list["MessageEvent"]] = relationship("MessageEvent")
    clients: Mapped[list["Client"]] = relationship("Client")

    def __repr__(self) -> str:
        return self.name
