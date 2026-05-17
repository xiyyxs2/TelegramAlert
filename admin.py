from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from config import config, get_channel_id
from database import set_paused, is_paused, count_today_posts, get_active_alerts, get_stat
from random_posts import send_random_post, send_blog_post
from alerts import send_alert, send_clear, send_update
from wave import send_wave
from weather import send_weather

router = Router()


def admin_only(message: Message) -> bool:
    return bool(message.from_user and message.from_user.id == config.ADMIN_ID)


@router.message(Command("start"))
async def start_cmd(message: Message):
    if not admin_only(message):
        return await message.answer("Нет доступа.")
    await message.answer(
        "Бот запущен.\n"
        "Команды: /status /pause /resume /test_post /test_blog /test_alert /test_clear /test_update /test_wave /test_weather"
    )


@router.message(Command("status"))
async def status_cmd(message: Message):
    if not admin_only(message):
        return await message.answer("Нет доступа.")
    paused = await is_paused()
    today = await count_today_posts()
    active = await get_active_alerts()
    planned = await get_stat("planned_jobs", "невідомо")
    await message.answer(
        f"Статус: {'пауза' if paused else 'працює'}\n"
        f"Постів сьогодні: {today}\n"
        f"Активних тривог: {len(active)}\n"
        f"Заплановано jobs: {planned}\n"
        f"Канал: {get_channel_id()}"
    )


@router.message(Command("pause"))
async def pause_cmd(message: Message):
    if not admin_only(message):
        return await message.answer("Нет доступа.")
    await set_paused(True)
    await message.answer("Автопостинг поставлено на паузу.")


@router.message(Command("resume"))
async def resume_cmd(message: Message):
    if not admin_only(message):
        return await message.answer("Нет доступа.")
    await set_paused(False)
    await message.answer("Автопостинг увімкнено.")


@router.message(Command("test_post"))
async def test_post_cmd(message: Message):
    if not admin_only(message):
        return await message.answer("Нет доступа.")
    await send_random_post(message.bot, get_channel_id())
    await message.answer("Тестовий пост відправлено.")


@router.message(Command("test_blog"))
async def test_blog_cmd(message: Message):
    if not admin_only(message):
        return await message.answer("Нет доступа.")
    await send_blog_post(message.bot, get_channel_id())
    await message.answer("Блог-пост відправлено.")


@router.message(Command("test_alert"))
async def test_alert_cmd(message: Message):
    if not admin_only(message):
        return await message.answer("Нет доступа.")
    await send_alert(message.bot, get_channel_id())
    await message.answer("Тривогу відправлено.")


@router.message(Command("test_clear"))
async def test_clear_cmd(message: Message):
    if not admin_only(message):
        return await message.answer("Нет доступа.")
    await send_clear(message.bot, get_channel_id())
    await message.answer("Відбій відправлено.")


@router.message(Command("test_update"))
async def test_update_cmd(message: Message):
    if not admin_only(message):
        return await message.answer("Нет доступа.")
    await send_update(message.bot, get_channel_id())
    await message.answer("Оновлення відправлено.")


@router.message(Command("test_wave"))
async def test_wave_cmd(message: Message):
    if not admin_only(message):
        return await message.answer("Нет доступа.")
    await send_wave(message.bot, get_channel_id())
    await message.answer("Хвилю відправлено.")


@router.message(Command("test_weather"))
async def test_weather_cmd(message: Message):
    if not admin_only(message):
        return await message.answer("Нет доступа.")
    await send_weather(message.bot, get_channel_id())
    await message.answer("Погоду відправлено.")
