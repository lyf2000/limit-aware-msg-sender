from typing import TYPE_CHECKING
from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped, relationship

from db.models.base import BaseModel


if TYPE_CHECKING:
    from db.models.platform import Platform


class ConversationType(BaseModel):
    __tablename__ = "conversation_types"
    __table_args__ = (UniqueConstraint("key", "platform_id"),)

    name = mapped_column(String(64), nullable=False)
    key = mapped_column(String(64), nullable=False)

    platform_id = mapped_column(ForeignKey("platforms.id"), nullable=False)
    platform: Mapped["Platform"] = relationship("Platform", uselist=False)

    rules: Mapped[list["ConversationRule"]] = relationship("ConversationRule")


class ConversationRule(BaseModel):
    __tablename__ = "conversation_rules"

    conversation_type_id = mapped_column(ForeignKey("conversation_types.id"), nullable=False)
    conversation: Mapped["ConversationType"] = relationship("ConversationType", uselist=False)

    period = mapped_column(Integer(), nullable=False)
    available = mapped_column(Integer(), nullable=False)
    per_chat = mapped_column(Boolean(), nullable=False)
