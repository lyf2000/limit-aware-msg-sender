from db.models.platform import Platform
from db.service.base import BaseModelService


class PlatformModelService(BaseModelService):
    MODEL = Platform
