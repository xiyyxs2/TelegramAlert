import random
from alerts import random_region
from database import log_post

WAVE_TEMPLATES = [
    "🌊 Зафіксована енергетична хвиля.\nІнтенсивність: {percent}%\nДжерело: {region}.",
    "🌊 По моніторингу проходить хвиля.\nСила: {percent}%\nЙмовірне джерело: {region}.",
    "🌀 Дивна хвиля пішла з боку {region}.\nІнтенсивність приблизно {percent}%.",
    "🌊 {region}: фон піднявся до {percent}%. Спостерігаємо.",
]


def build_wave() -> str:
    return random.choice(WAVE_TEMPLATES).format(
        percent=random.randint(10, 100),
        region=random_region(),
    )


async def send_wave(bot, channel_id):
    text = build_wave()
    await bot.send_message(channel_id, text)
    await log_post("wave", text)
