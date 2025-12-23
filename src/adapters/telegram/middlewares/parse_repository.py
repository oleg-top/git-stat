from aiogram import BaseMiddleware
from typing import Callable, Awaitable
from aiogram.types import TelegramObject

from app.use_cases.dummy_parse_repository import ParseRepositoryUseCase


class ParseRepositoryMiddleware(BaseMiddleware):
    def __init__(self, parse_repo_uc: ParseRepositoryUseCase):
        super().__init__()
        self.parse_repo_uc = parse_repo_uc

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable],
        event: TelegramObject,
        data: dict,
    ):
        data["parse_repo_uc"] = self.parse_repo_uc
        return await handler(event, data)
