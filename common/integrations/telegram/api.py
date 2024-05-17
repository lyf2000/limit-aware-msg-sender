import aiohttp
from common.client import METHODS
from common.integrations.base import BaseApiClient, SchemaResponseBodyDecorator
from common.integrations.telegram.schema import TelegramChat


class TelegramApiClient(BaseApiClient):
    HEADERS = {
        "Content-Type": "application/json",
    }

    def __init__(self, token: str) -> None:
        super().__init__()
        self.token = token

    def _get_url(self, method: str, url_kwargs: dict) -> str:
        query_p = ""
        if url_kwargs:
            query_p = "?" + "&".join(f"{k}={v}" for k, v in url_kwargs.items())
        return f"https://api.telegram.org/bot{self.token}/{method}{query_p}"

    async def _method(
        self, method: METHODS, tg_method: str, url_kwargs: dict, data: dict | None = None
    ) -> aiohttp.ClientRequest:
        url = self._get_url(tg_method, url_kwargs)
        return await super()._method(method, url, data)

    @SchemaResponseBodyDecorator(TelegramChat)
    async def get_chat_info(self, chat_id: int) -> TelegramChat:
        return await self._method("post", "getChat", url_kwargs=dict(chat_id=chat_id))
