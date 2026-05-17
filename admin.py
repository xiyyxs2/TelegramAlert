from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from config import Config
import database
from scheduler import planned_jobs_count, publish_random_post, publish_alert, publish_clear, publish_wave, publish_weather

router = Router()


def admin_only(cfg: Config, message: Message) -> bool:
    return bool(message.from_user and message.from_user.id == cfg.admin_id)


@router.message(Command("start"))
async def start(message: Message, cfg: Config) -> None:
    if not admin_only(cfg, message):
        return
    await message.answer(
        "Бот запущен в пассивном режиме.\n"
        "Команды: /status /pause /resume /test_post /test_alert /test_clear /test_wave /test_weather"
    )


@router.message(Command("status"))
async def status(message: Message, cfg: Config) -> None:
    if not admin_only(cfg, message):
        return
    await message.answer(
        f"Статус: {'пауза' if database.is_paused() else 'активен'}\n"
        f"Запланировано jobs: {planned_jobs_count()}\n"
        f"Активных тревог: {database.count_active_alerts()}\n"
        f"Канал: {cfg.channel_id}"
    )


@router.message(Command("pause"))
async def pause(message: Message, cfg: Config) -> None:
    if not admin_only(cfg, message):
        return
    database.set_paused(True)
    await message.answer("Автопостинг остановлен.")


@router.message(Command("resume"))
async def resume(message: Message, cfg: Config) -> None:
    if not admin_only(cfg, message):
        return
    database.set_paused(False)
    await message.answer("Автопостинг включён.")


@router.message(Command("test_post"))
async def test_post(message: Message, bot: Bot, cfg: Config) -> None:
    if not admin_only(cfg, message):
        return
    await publish_random_post(bot, cfg)
    await message.answer("Случайный пост отправлен.")


@router.message(Command("test_alert"))
async def test_alert(message: Message, bot: Bot, cfg: Config) -> None:
    if not admin_only(cfg, message):
        return
    await publish_alert(bot, cfg)
    await message.answer("Тревога отправлена.")


@router.message(Command("test_clear"))
async def test_clear(message: Message, bot: Bot, cfg: Config) -> None:
    if not admin_only(cfg, message):
        return
    await publish_clear(bot, cfg)
    await message.answer("Отбой отправлен.")


@router.message(Command("test_wave"))
async def test_wave(message: Message, bot: Bot, cfg: Config) -> None:
    if not admin_only(cfg, message):
        return
    await publish_wave(bot, cfg)
    await message.answer("Волна отправлена.")


@router.message(Command("test_weather"))
async def test_weather(message: Message, bot: Bot, cfg: Config) -> None:
    if not admin_only(cfg, message):
        return
    await publish_weather(bot, cfg)
    await message.answer("Погода отправлена.")
