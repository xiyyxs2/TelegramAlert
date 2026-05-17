import random
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo
from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from apscheduler.triggers.cron import CronTrigger

from config import Config
import database
from alerts import make_alert, make_clear, make_update, make_odd_message, start_alert_in_db, pop_random_alert
from random_posts import make_regular_post, make_blog_post
from wave import make_wave
from weather import get_weather_text

scheduler = AsyncIOScheduler()


async def publish(bot: Bot, cfg: Config, post_type: str, text: str) -> None:
    if database.is_paused():
        return
    await bot.send_message(cfg.channel_id, text)
    database.log_post(post_type, text)


async def publish_random_post(bot: Bot, cfg: Config) -> None:
    kind = random.choices(
        ["regular", "blog", "odd", "update", "weather", "wave"],
        weights=[35, 15, 20, 12, 10, 8],
        k=1,
    )[0]
    if kind == "regular":
        await publish(bot, cfg, "regular", make_regular_post(cfg.simulation_label))
    elif kind == "blog":
        await publish(bot, cfg, "blog", make_blog_post(cfg.simulation_label))
    elif kind == "odd":
        await publish(bot, cfg, "odd", make_odd_message(cfg.simulation_label))
    elif kind == "update":
        await publish(bot, cfg, "update", make_update(cfg.simulation_label))
    elif kind == "weather":
        await publish(bot, cfg, "weather", await get_weather_text(cfg.weather_key, cfg.simulation_label))
    else:
        await publish(bot, cfg, "wave", make_wave(cfg.simulation_label))


async def publish_alert(bot: Bot, cfg: Config) -> None:
    region, threat, text = make_alert(cfg.simulation_label)
    start_alert_in_db(region, threat)
    await publish(bot, cfg, "alert", text)


async def publish_clear(bot: Bot, cfg: Config) -> None:
    popped = pop_random_alert()
    if not popped:
        region, _, _ = make_alert(cfg.simulation_label)
    else:
        _, region = popped
    await publish(bot, cfg, "clear", make_clear(region, cfg.simulation_label))


async def publish_wave(bot: Bot, cfg: Config) -> None:
    await publish(bot, cfg, "wave", make_wave(cfg.simulation_label))


async def publish_weather(bot: Bot, cfg: Config) -> None:
    await publish(bot, cfg, "weather", await get_weather_text(cfg.weather_key, cfg.simulation_label))


def _random_daytime(tz: ZoneInfo) -> datetime:
    now = datetime.now(tz)
    hour = random.choices(
        list(range(24)),
        weights=[1,1,1,1,1,2,3,5,7,8,8,8,8,8,8,8,7,7,6,5,4,3,2,1],
        k=1,
    )[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    dt = datetime.combine(now.date(), time(hour, minute, second), tzinfo=tz)
    if dt <= now + timedelta(seconds=30):
        dt = now + timedelta(minutes=random.randint(1, 90))
    return dt


def _add_job(coro, run_at: datetime, *args) -> None:
    scheduler.add_job(coro, DateTrigger(run_date=run_at), args=args, misfire_grace_time=300)


async def plan_day(bot: Bot, cfg: Config) -> None:
    tz = ZoneInfo(cfg.timezone)
    scheduler.remove_all_jobs()
    scheduler.add_job(plan_day, CronTrigger(hour=0, minute=5, timezone=tz), args=[bot, cfg], id="daily_replan", replace_existing=True)

    posts_count = random.randint(cfg.min_posts_per_day, cfg.max_posts_per_day)
    for _ in range(posts_count):
        _add_job(publish_random_post, _random_daytime(tz), bot, cfg)

    alert_count = random.randint(2, 6)
    for _ in range(alert_count):
        alert_time = _random_daytime(tz)
        clear_time = alert_time + timedelta(minutes=random.randint(15, 120))
        _add_job(publish_alert, alert_time, bot, cfg)
        _add_job(publish_clear, clear_time, bot, cfg)
        if random.random() < 0.65:
            upd_time = alert_time + timedelta(minutes=random.randint(5, 60))
            if upd_time < clear_time:
                _add_job(publish_random_post, upd_time, bot, cfg)

    for _ in range(random.randint(1, 3)):
        _add_job(publish_wave, _random_daytime(tz), bot, cfg)

    morning = datetime.combine(datetime.now(tz).date(), time(random.randint(7, 10), random.randint(0, 59)), tzinfo=tz)
    if morning > datetime.now(tz):
        _add_job(publish_weather, morning, bot, cfg)


def planned_jobs_count() -> int:
    return len(scheduler.get_jobs())


async def start_scheduler(bot: Bot, cfg: Config) -> None:
    if not scheduler.running:
        scheduler.configure(timezone=cfg.timezone)
        scheduler.start()
    await plan_day(bot, cfg)
