from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped, relationship

from db.models.base import BaseModel


if TYPE_CHECKING:
    from db.models.message import MessageEvent
    from db.models.platform import Platform


class Client(BaseModel):
    __tablename__ = "clients"
    __table_args__ = (UniqueConstraint("platform_id", "token"),)

    name = mapped_column(String(64), nullable=False)
    token = mapped_column(String(256), nullable=False)

    platform_id = mapped_column(ForeignKey("platforms.id"), nullable=False)
    platform: Mapped["Platform"] = relationship("Platform", uselist=False)

    message_events: Mapped[list["MessageEvent"]] = relationship("Platform")
