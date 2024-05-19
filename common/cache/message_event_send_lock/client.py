from datetime import datetime
from db.models.message import MessageEvent
from db.models.conversation import ConversationRule

from cache.redis.api import BaseDetailRedisClient, CacheValue, InitValueCacheMixin
from db.models.conversation import ConversationRule
from db.models.message import MessageEvent


class RuleSendMessageLockDetailRedisApi(InitValueCacheMixin, BaseDetailRedisClient):
    async def __init__(self, message_event: MessageEvent, rule: ConversationRule):
        await super().__init__()
        self.message_event = message_event
        self.rule = rule

    async def exp(self) -> int:
        return self.rule.period

    async def decr(self):
        await self.set(await self.get() - 1)

    async def _get_key(self) -> str:
        head_key = f"message.lock.{self.message_event.client_id}.{self.rule.id}"
        if self.rule.per_chat:
            return head_key + f".{self.message_event.chat_id}"
        return head_key

    async def _init_value_to_cache(self) -> CacheValue:
        return self.rule.available

    async def _parse_to_value(self, value: CacheValue) -> int:
        return int(await super()._parse_to_value(value))
