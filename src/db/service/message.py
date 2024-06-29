from db.models.message import MessageEvent
from db.service.base import BaseModelService


class MessageModelService(BaseModelService):
    MODEL = MessageEvent
