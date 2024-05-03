from typing import Type
from common.service.senders.base import BaseSenderService
from common.service.senders.telegram import TelegramMessageSenderService
from common.service.senders.vk import VkMessageSenderService
from db.models.platform import PlatformTypeChoices


MESSAGE_SERVICE_PLATFORM_TYPE_MAP: dict[int, Type[BaseSenderService]] = {
    PlatformTypeChoices.TELEGRAM: TelegramMessageSenderService,
    PlatformTypeChoices.VK: VkMessageSenderService,
}
