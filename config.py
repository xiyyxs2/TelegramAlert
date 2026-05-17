import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except ValueError:
        return default


@dataclass(frozen=True)
class Config:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN", "").strip()
    ADMIN_ID: int = _int("ADMIN_ID", 0)
    CHANNEL_ID: str = os.getenv("CHANNEL_ID", "").strip()
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "").strip()
    TIMEZONE: str = os.getenv("TIMEZONE", "Europe/Kyiv").strip()
    DEFAULT_CITY: str = os.getenv("DEFAULT_CITY", "Київ").strip()
    MIN_POSTS_PER_DAY: int = _int("MIN_POSTS_PER_DAY", 15)
    MAX_POSTS_PER_DAY: int = _int("MAX_POSTS_PER_DAY", 45)
    DB_PATH: str = os.getenv("DB_PATH", "bot.db").strip()
    REPEAT_OLD_POST_CHANCE: int = _int("REPEAT_OLD_POST_CHANCE", 18)


config = Config()


def get_channel_id():
    value = config.CHANNEL_ID
    if value.startswith("@"):
        return value
    try:
        return int(value)
    except ValueError:
        return value
