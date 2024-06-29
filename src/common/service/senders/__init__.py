from typing import Type
from common.service.senders.base import BaseSenderService
from common.service.senders.telegram.sender import TelegramMessageSenderService
from common.service.senders.vk import VkMessageSenderService
from db.models.platform import PlatformTypeChoices
