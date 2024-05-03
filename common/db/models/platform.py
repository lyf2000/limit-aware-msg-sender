from typing import TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped, relationship

from common.db.models.base import BaseModel


if TYPE_CHECKING:
    from common.db.models.conversation import ConversationType
    from common.db.models.message import MessageEvent
    from common.db.models.client import Client


class Platform(BaseModel):
    __tablename__ = "platforms"

    name = mapped_column(String(64), nullable=False)

    conversation_types: Mapped[list["ConversationType"]] = relationship("ConversationType")
    message_events: Mapped[list["MessageEvent"]] = relationship("MessageEvent")
    clients: Mapped[list["Client"]] = relationship("Client")

    def __repr__(self) -> str:
        return self.name
