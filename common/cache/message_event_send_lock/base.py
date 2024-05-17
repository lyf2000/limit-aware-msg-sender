from db.models.message import MessageEvent
from db.models.conversation import ConversationRule

from cache.redis.api import BaseDetailRedisApi, CacheValue
from db.models.conversation import ConversationRule
from db.models.message import MessageEvent


class RuleSendMessageLockDetailRedisApi(BaseDetailRedisApi):
    async def __init__(self, message_event: MessageEvent, rule: ConversationRule):
        await super().__init__()
        self.message_event = message_event
        self.rule = rule

    async def _get_key(self) -> str:
        head_key = f"message.lock.{self.message_event.client_id}.{self.rule.id}"
        if self.rule.per_chat:
            return head_key + f".{self.message_event.chat_id}"
        return head_key

    async def _value_to_cache(self) -> CacheValue:
        return self.rule.available

    async def _cache_to_value(self, value: CacheValue) -> CacheValue:
        return int(await super()._cache_to_value(value))

    async def get(self):
        if (result := await super().get()) is None:
            await self.set()
            return await self.get()
        return result
