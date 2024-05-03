# Decentrelazed locking


from db.connection import get_session
from db.models.message import MessageEvent
from db.models.conversation import ConversationRule
from db.service.conversation import ConversationRuleModelService


class LimitLockService:
    def __init__(self, message_event: MessageEvent) -> None:
        self.message_event = message_event

    async def can_send(self) -> bool:
        return True

    async def rules(self) -> list[ConversationRule]:
        q = ConversationRuleModelService.from_message_event(
            type=self.message_event.type,
            client_id=self.message_event.client_id,
        )
        return list((await get_session().execute(q)).all())
