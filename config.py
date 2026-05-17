from dataclasses import dataclass
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def _int_env(name: str, default: int) -> int:
    try:
        return int(getenv(name, str(default)))
    except ValueError:
        return default


@dataclass(frozen=True)
class Config:
    bot_token: str
    admin_id: int
    channel_id: str
    weather_key: str
    timezone: str
    min_posts_per_day: int
    max_posts_per_day: int
    simulation_label: bool


def load_config() -> Config:
    token = getenv("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("BOT_TOKEN is empty. Add it to .env or Railway Variables.")

    return Config(
        bot_token=token,
        admin_id=_int_env("ADMIN_ID", 0),
        channel_id=getenv("CHANNEL_ID", "").strip(),
        weather_key=getenv("OPENWEATHER_API_KEY", "").strip(),
        timezone=getenv("TIMEZONE", "Europe/Kyiv").strip(),
        min_posts_per_day=_int_env("MIN_POSTS_PER_DAY", 15),
        max_posts_per_day=_int_env("MAX_POSTS_PER_DAY", 45),
        simulation_label=getenv("SIMULATION_LABEL", "false").strip().lower() in {"1", "true", "yes", "y"},
    )
