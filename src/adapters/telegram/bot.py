import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from adapters.telegram.middlewares.add_repository import AddRepositoryMiddleware
from adapters.telegram.middlewares.parse_repository import ParseRepositoryMiddleware
from adapters.telegram.middlewares.user_repositories import UserRepositoriesMiddleware
from app.use_cases.add_user_repository import AddUserRepositoryUseCase
from app.use_cases.dummy_parse_repository import ParseRepositoryUseCase
from config import config
from domain.models.filterer import DefaultRepositoryFilterer
from domain.parsing.stream_parser import StreamFileParser
from handlers.start import router as start_router
from handlers.add_repo import router as add_repo_router
from handlers.list_repo import router as list_repo_router
from handlers.remove_repo import router as remove_repo_router
from handlers.common import router as common_router
from handlers.stats import router as stats_router
from infra.cache.redis.client import RedisClient
from infra.cache.redis.user_repos import RedisUserRepositories
from infra.git.file_converter import GitFileConverter
from infra.storage.local.storage import LocalGitRepositoryStorage

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    config.validate()

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    redis_client = RedisClient(host=config.REDIS_HOST, port=int(config.REDIS_PORT))

    user_repos_storage = RedisUserRepositories(redis_client)
    repo_storage = LocalGitRepositoryStorage()
    file_converter = GitFileConverter()
    filterer = DefaultRepositoryFilterer()
    stream_parser = StreamFileParser()

    add_repo_uc = AddUserRepositoryUseCase(user_repos_storage, repo_storage)
    parse_repo_uc = ParseRepositoryUseCase(repo_storage, file_converter, filterer, stream_parser)

    dp.update.middleware(AddRepositoryMiddleware(add_repo_uc))
    dp.update.middleware(UserRepositoriesMiddleware(user_repos_storage))
    dp.update.middleware(ParseRepositoryMiddleware(parse_repo_uc))

    logger.info("📡 Подключаем роутеры...")

    dp.include_router(start_router)
    dp.include_router(add_repo_router)
    dp.include_router(stats_router)

    dp.include_router(list_repo_router)
    dp.include_router(remove_repo_router)

    dp.include_router(common_router)

    logger.info("🤖 Бот запускается...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
