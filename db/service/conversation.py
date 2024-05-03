from db.models.conversation import ConversationRule, ConversationType
from db.service.base import BaseModelService


class ConversationRuleModelService(BaseModelService):
    MODEL = ConversationRule

    @classmethod
    def from_message_event(cls, type: int, client_id: int):
        return (
            cls.select_by()
            .join(ConversationType)
            .where(
                ConversationType.key == type,
            )
        )
