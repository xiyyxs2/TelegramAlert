import random
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
from config import config, get_channel_id
from database import is_paused, set_stat
from random_posts import send_random_post, send_blog_post
from alerts import send_alert, send_clear, send_update
from wave import send_wave
from weather import send_weather

scheduler = AsyncIOScheduler(timezone=ZoneInfo(config.TIMEZONE))


async def guarded(job_func, bot, *args):
    if await is_paused():
        return
    channel_id = get_channel_id()
    try:
        await job_func(bot, channel_id, *args)
    except Exception as e:
        print(f"Job error {job_func.__name__}: {e}")


def random_time_today(tz: ZoneInfo) -> datetime:
    now = datetime.now(tz)
    start = now + timedelta(minutes=2)
    end = datetime.combine(now.date(), time(23, 55), tzinfo=tz)
    if start >= end:
        return now + timedelta(minutes=random.randint(2, 20))

    # День активнее, ночь реже
    hour_pool = [0, 1, 2, 3, 4, 5] * 1 + [6, 7, 8, 9] * 2 + list(range(10, 23)) * 4 + [23] * 2
    for _ in range(40):
        h = random.choice(hour_pool)
        m = random.randint(0, 59)
        dt = datetime.combine(now.date(), time(h, m), tzinfo=tz)
        if start <= dt <= end:
            return dt
    seconds = random.randint(0, int((end - start).total_seconds()))
    return start + timedelta(seconds=seconds)


async def alert_sequence(bot):
    if await is_paused():
        return
    channel_id = get_channel_id()
    region = await send_alert(bot, channel_id)
    if random.randint(1, 100) <= 45:
        delay_update = random.randint(4, 25)
        scheduler.add_job(
            guarded,
            DateTrigger(run_date=datetime.now(ZoneInfo(config.TIMEZONE)) + timedelta(minutes=delay_update)),
            args=[send_update, bot, region],
            id=f"update_{region}_{random.randint(1000,9999)}",
            replace_existing=False,
        )
    delay_clear = random.randint(15, 120)
    scheduler.add_job(
        guarded,
        DateTrigger(run_date=datetime.now(ZoneInfo(config.TIMEZONE)) + timedelta(minutes=delay_clear)),
        args=[send_clear, bot, region],
        id=f"clear_{region}_{random.randint(1000,9999)}",
        replace_existing=False,
    )


async def plan_today(bot):
    tz = ZoneInfo(config.TIMEZONE)
    for job in list(scheduler.get_jobs()):
        if job.id.startswith("auto_") or job.id.startswith("alertseq_") or job.id.startswith("wave_") or job.id.startswith("weather_"):
            scheduler.remove_job(job.id)

    posts_count = random.randint(config.MIN_POSTS_PER_DAY, config.MAX_POSTS_PER_DAY)
    alert_count = random.randint(2, 6)
    wave_count = random.randint(1, 3)

    for i in range(posts_count):
        roll = random.randint(1, 100)
        func = send_blog_post if roll <= 22 else send_random_post
        scheduler.add_job(
            guarded,
            DateTrigger(run_date=random_time_today(tz)),
            args=[func, bot],
            id=f"auto_post_{i}_{random.randint(1000,9999)}",
            replace_existing=False,
        )

    for i in range(alert_count):
        scheduler.add_job(
            alert_sequence,
            DateTrigger(run_date=random_time_today(tz)),
            args=[bot],
            id=f"alertseq_{i}_{random.randint(1000,9999)}",
            replace_existing=False,
        )

    for i in range(wave_count):
        scheduler.add_job(
            guarded,
            DateTrigger(run_date=random_time_today(tz)),
            args=[send_wave, bot],
            id=f"wave_{i}_{random.randint(1000,9999)}",
            replace_existing=False,
        )

    scheduler.add_job(
        guarded,
        DateTrigger(run_date=random_time_today(tz)),
        args=[send_weather, bot],
        id=f"weather_{random.randint(1000,9999)}",
        replace_existing=False,
    )
    await set_stat("planned_jobs", str(len(scheduler.get_jobs())))
    print(f"Daily plan created: {posts_count} posts, {alert_count} alerts, {wave_count} waves")


def setup_scheduler(bot):
    if not scheduler.running:
        scheduler.start()
    scheduler.add_job(
        plan_today,
        CronTrigger(hour=0, minute=5, timezone=ZoneInfo(config.TIMEZONE)),
        args=[bot],
        id="daily_replan",
        replace_existing=True,
    )
