from common.client import BaseClient


class TelegramClient(BaseClient):
    HEADERS = {
        "Content-Type": "application/json",
    }
