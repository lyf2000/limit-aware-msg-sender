from sqlalchemy import and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from common.integrations.gateway import PlatformIntegrationGateway
from common.integrations.telegram.api import TelegramApiClient
from db.models.conversation import ConversationRule, ConversationType
from db.models.message import MessageEvent
from db.service.base import BaseModelService


class ConversationTypeModelService(BaseModelService):
    MODEL = ConversationType

    @classmethod
    async def get_by_type(cls, platform_id: int, type: str, session: AsyncSession | None = None):
        q = cls.get(cls.select(cls.MODEL).filter(platform_id=platform_id, key=type))
        return await cls.get(q, session)


class ConversationRuleModelService(BaseModelService):
    MODEL = ConversationRule

    @classmethod
    async def get_list_for_message_event(
        cls, message_event: MessageEvent, session: AsyncSession | None = None, as_q=False
    ) -> list[ConversationRule]:
        chat_type = await PlatformIntegrationGateway(message_event).get_chat_type()
        q = (
            cls.select(cls.MODEL)
            .join(ConversationType)
            .filter(
                or_(
                    and_(ConversationType.key == chat_type, ConversationRule.per_chat == True),
                    ConversationRule.per_chat == False,
                ),
            )
        )

        if as_q:
            return q

        return list(await cls.list(q, session))
