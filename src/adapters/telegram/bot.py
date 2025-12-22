import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import config

from handlers import (
    start_router,
    add_repo_router,
    list_repo_router,
    remove_repo_router,
    common_router
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def main():
    config.validate()

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    logger.info("📡 Подключаем роутеры...")

    dp.include_router(start_router)
    dp.include_router(add_repo_router)

    dp.include_router(list_repo_router)
    dp.include_router(remove_repo_router)

    dp.include_router(common_router)

    logger.info("🤖 Бот запускается...")
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
