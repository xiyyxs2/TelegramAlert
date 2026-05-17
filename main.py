import asyncio
from aiogram import Bot, Dispatcher
from config import config
from database import init_db
from admin import router
from scheduler import setup_scheduler, plan_today


async def main():
    if not config.BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing. Add it to Railway Variables or .env")
    if not config.CHANNEL_ID:
        raise RuntimeError("CHANNEL_ID is missing. Add it to Railway Variables or .env")
    if not config.ADMIN_ID:
        print("Warning: ADMIN_ID is empty. Admin commands will not work.")

    await init_db()

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    setup_scheduler(bot)
    await plan_today(bot)

    print("Bot started")
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
