import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import load_config
import database
from admin import router as admin_router
from scheduler import start_scheduler


async def main() -> None:
    logging.basicConfig(level=logging.INFO)
    cfg = load_config()
    database.init_db(cfg.channel_id)

    bot = Bot(token=cfg.bot_token)
    dp = Dispatcher()
    dp["cfg"] = cfg
    dp.include_router(admin_router)

    await start_scheduler(bot, cfg)
    await dp.start_polling(bot, cfg=cfg)


if __name__ == "__main__":
    asyncio.run(main())
