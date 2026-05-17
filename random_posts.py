import random
from config import config
from database import get_recent_posts, log_post
from humanizer import prepare_message
from alerts import random_region

NORMAL_POSTS = [
    "Моніторинг триває",
    "Поки без різких змін",
    "Інформація уточнюється",
    "При наближенні попередимо",
    "Локаційно зник",
    "Збиття. 🟨",
    "Кружляє 1 мопед",
    "Дорозвідка по цілях",
    "Поки без підтвердження",
    "Наразі спостерігаємо",
    "Станом на зараз без критичних оновлень",
    "Рух є, але поки без конкретики",
    "По напрямку тихо",
    "Працюємо по моніторингу",
    "Звʼязок є, оновлення будуть",
    "Якщо буде щось важливе — напишемо",
    "Є активність, не розганяємо зайве",
    "Поки просто тримаємо на контролі",
    "Ніч пройшла відносно спокійно",
    "День поки без різких змін",
    "Коротко: моніторинг є, паніки немає",
]

REGION_POSTS = [
    "{region}: дорозвідка, не розганяємо зайве",
    "По {region} є рух",
    "{region}: ситуація без різких змін",
    "У районі {region} поки тихо",
    "{region} на моніторингу",
    "По {region} інформація уточнюється",
    "{region}: якщо буде наближення — попередимо",
    "На {region} поки без підтвердження",
    "{region}: локаційно зник",
]

BLOG_UA = [
    "Міні-влог моніторингу: відкрив карту, подивився на {region}, закрив карту, відкрив знову",
    "Сиджу на моніторингу, по {region} поки без жорстких новин",
    "Коротко по каналу: живі, дивимось, оновлення будуть",
    "День якийсь рівний, але {region} все одно тримаємо на оці",
    "Наразі все виглядає спокійніше, ніж могло б бути",
    "Відписую коротко: моніторинг іде, якщо щось буде — кину сюди",
]

BLOG_MULTI = [
    "English update: monitoring continues. {region} still on watch",
    "العربية تقول: لا يوجد تأكيد حتى الآن. {region} під наглядом",
    "Español update: seguimos mirando {region}, sin confirmación fuerte",
    "Français: {region} reste en observation, rien de critique pour le moment",
    "Deutsch kurz: {region} bleibt im Monitoring, aktuell ohne harte Bestätigung",
    "Polski update: {region} pod obserwacją, bez większych zmian",
    "日本語ミニ更新: {region} はまだ監視中です",
    "한국어 업데이트: {region} 계속 모니터링 중",
    "中文简报：{region} 仍在监测中，目前没有明确确认",
]


def build_random_post() -> str:
    region = random_region()
    if random.randint(1, 100) <= 45:
        return random.choice(REGION_POSTS).format(region=region)
    return random.choice(NORMAL_POSTS)


def build_blog_post() -> str:
    region = random_region()
    bank = BLOG_UA if random.randint(1, 100) <= 60 else BLOG_MULTI
    return random.choice(bank).format(region=region)


async def maybe_repeat_old_post():
    if random.randint(1, 100) > config.REPEAT_OLD_POST_CHANCE:
        return None
    old = await get_recent_posts(40)
    old = [p for p in old if p and len(p) <= 600]
    if not old:
        return None
    return random.choice(old)


async def send_random_post(bot, channel_id):
    repeated = await maybe_repeat_old_post()
    if repeated:
        text = repeated
        post_type = "repeat"
    else:
        text = prepare_message(build_random_post(), "regular")
        post_type = "regular"
    await bot.send_message(channel_id, text)
    await log_post(post_type, text)


async def send_blog_post(bot, channel_id):
    text = prepare_message(build_blog_post(), "blog")
    await bot.send_message(channel_id, text)
    await log_post("blog", text)
