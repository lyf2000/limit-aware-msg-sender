# Decentrelazed locking
from common.cache.message_event_send_lock.base import RuleSendMessageLockDetailRedisApi
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
            (False for rule in await self._rules() if (await get_rule_available(rule)) < 0),
            True,
        )

    async def bb(self):
        async def get_rule_available(rule) -> int:
            return await (
                await RuleSendMessageLockDetailRedisApi(
                    message_event=self.message_event,
                    rule=rule,
                )
            ).get()

        return await get_rule_available((await self._rules())[0])

    async def _rules(self) -> list[ConversationRule]:
        return await ConversationRuleModelService.get_list_for_message_event(
            message_event=self.message_event,
            as_q=False,
        )
