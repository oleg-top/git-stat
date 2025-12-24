import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(env_path)


@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN')
    REDIS_HOST: str = os.getenv('REDIS_HOST')
    REDIS_PORT: str = os.getenv('REDIS_PORT')

    @classmethod
    def validate(cls):
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN environment variable is required")
        print("✅ Configuration loaded successfully")


config = Config()
