# Decentrelazed locking
from common.cache.message_event_send_lock.client import RuleSendMessageLockDetailRedisApi
from common.utils import asyncinit
from db.models.conversation import ConversationRule
from db.models.message import MessageEvent
from db.service.conversation import ConversationRuleModelService


class LimitMessageSendLockService:
    def __init__(self, message_event: MessageEvent) -> None:
        self.message_event = message_event

    async def can_send(self) -> bool:
        async def get_rule_available(rule) -> int:
            return await (
                await RuleSendMessageLockDetailRedisApi(
                    message_event=self.message_event,
                    rule=rule,
                )
            ).get()

        return await anext(
            (False for rule in await self._rules() if (await get_rule_available(rule)) < 1),
            True,
        )

    async def tried_send(self):
        """Decrement all rules' available."""

        async def decr(rule) -> int:
            return await (
                await RuleSendMessageLockDetailRedisApi(
                    message_event=self.message_event,
                    rule=rule,
                )
            ).decr()

        for rule in await self._rules():
            await decr(rule)

    async def _rules(self) -> list[ConversationRule]:
        return await ConversationRuleModelService.get_list_for_message_event(
            message_event=self.message_event,
            as_q=False,
        )
