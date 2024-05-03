from sqlalchemy_utils import ChoiceType
from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, SmallInteger, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped, relationship

from db.models.base import BaseModel


if TYPE_CHECKING:
    from db.models.client import Client


class MessageStatusChoices:
    WAITING = 0
    SENT = 1
    ERROR = -1

    CHOICES = (
        (WAITING, "waiting"),
        (SENT, "sent"),
        (ERROR, "error"),
    )


class MessageEvent(BaseModel):
    __tablename__ = "message_events"

    text = mapped_column(String, nullable=False, default="")
    type = mapped_column(String(64), nullable=False)

    status = mapped_column(
        ChoiceType(MessageStatusChoices.CHOICES, impl=SmallInteger),
        default=MessageStatusChoices.WAITING,
    )

    client_id = mapped_column(ForeignKey("clients.id"), nullable=False)
    client: Mapped["Client"] = relationship("Client", uselist=False)
