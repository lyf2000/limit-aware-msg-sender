from db.models.client import Client
from db.service.base import BaseModelService


class ClientModelService(BaseModelService):
    MODEL = Client
