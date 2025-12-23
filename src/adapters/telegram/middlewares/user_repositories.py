from aiogram import BaseMiddleware
from typing import Callable, Awaitable
from aiogram.types import TelegramObject

from domain.models.user_repos import UserRepositories


class UserRepositoriesMiddleware(BaseMiddleware):
    def __init__(self, user_repos: UserRepositories):
        super().__init__()
        self.user_repos = user_repos

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict], Awaitable],
        event: TelegramObject,
        data: dict,
    ):
        data["user_repos"] = self.user_repos
        return await handler(event, data)
