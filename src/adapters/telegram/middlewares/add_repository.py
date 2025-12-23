from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable, Awaitable

from app.use_cases.add_user_repository import AddUserRepositoryUseCase


class AddRepositoryMiddleware(BaseMiddleware):
    def __init__(self, add_repo_uc: AddUserRepositoryUseCase):
        super().__init__()
        self.add_repo_uc = add_repo_uc

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable],
        event: TelegramObject,
        data: dict,
    ):
        data["add_repo_uc"] = self.add_repo_uc
        return await handler(event, data)
