import random
from database import add_active_alert, pop_active_alert, log_post, clear_alert_by_region

ALERT_TEMPLATE = """🔴 ... - повітряна тривога!\n\n😇Підпишись. Повітряна тривога - Світ. Працює 24/7.\n📡 Куди летить? Завжди на звязку! Моніторинг | Радар📍🔫"""

CLEAR_TEMPLATE = """🟢... - відбій повітряної тривоги!\n\n😇Підпишись. Повітряна тривога - Світ. Працює 24/7.\n📡 Куди летить? Завжди на звязку! Моніторинг | Радар📍🔫"""

THREATS = [
    "крилата ракета",
    "балістична ракета",
    "гіперзвукова ракета",
    "рой дронів",
    "ударні БПЛА",
    "шахед-дрони",
    "розвідувальні БПЛА",
    "ракетний удар",
    "масований ракетний обстріл",
    "повітряна загроза",
    "невідомий літальний обʼєкт",
    "шахедне непорозуміння",
    "мопед",
    "обʼєкт",
]

REGIONS = [
    "Україна", "Польща", "Німеччина", "Франція", "Італія", "Іспанія", "Португалія", "Нідерланди", "Бельгія", "Швеція", "Норвегія", "Фінляндія", "Данія", "Литва", "Латвія", "Естонія", "Чехія", "Словаччина", "Австрія", "Угорщина", "Румунія", "Молдова", "Болгарія", "Греція", "Туреччина", "Грузія", "Вірменія", "Азербайджан", "Казахстан", "Узбекистан", "Киргизстан", "Таджикистан", "Туркменістан", "Монголія", "Китай", "Японія", "Південна Корея", "Північна Корея", "Індія", "Пакистан", "Афганістан", "Іран", "Ірак", "Сирія", "Ліван", "Йорданія", "Ізраїль", "Саудівська Аравія", "ОАЕ", "Катар", "Кувейт", "Оман", "Ємен", "Єгипет", "Лівія", "Туніс", "Алжир", "Марокко", "Судан", "Ефіопія", "Кенія", "Танзанія", "Уганда", "ДР Конго", "Нігерія", "Гана", "Сенегал", "Малі", "Нігер", "Чад", "ПАР", "Мадагаскар", "США", "Канада", "Мексика", "Бразилія", "Аргентина", "Чилі", "Перу", "Колумбія", "Венесуела", "Болівія", "Австралія", "Нова Зеландія", "Індонезія", "Філіппіни", "Таїланд", "Вʼєтнам", "Малайзія", "Сінгапур", "Антарктика",
    "Київ", "Харків", "Одеса", "Дніпро", "Львів", "Запоріжжя", "Лондон", "Париж", "Берлін", "Рим", "Мадрид", "Каїр", "Токіо", "Сеул", "Нью-Йорк", "Торонто", "Сідней",
    "Пушенленд", "Пошона", "Луна", "Марс", "Галактика 67", "Галактика 69", "Сектор Омега", "Внешний пояс колоний", "Внутрішній купол", "Зона 404", "Північний кратер", "Південна башта", "Старий радар", "Туманний сектор", "Архівний пояс", "Сектор Нуль", "Портал 12", "Зелений коридор", "Чорний маяк", "Східний Схід", "Весь Світ", "Єгипетський район", "Галактика \"КукінД\"",
]

UPDATE_TEMPLATES = [
    "{region}: дорозвідка по цілях.",
    "По {region} є рух, спостерігаємо.",
    "{region}: поки без підтвердження, моніторинг триває.",
    "При наближенні до {region} попередимо.",
    "Кружляє 1 мопед біля {region}.",
    "Локаційно зник у районі {region}.",
    "Збиття по напрямку {region}. 🟨",
    "На {region} йде дорозвідка.",
    "По {region} без різких змін, але тримаємо на контролі.",
    "{region}: інформація уточнюється.",
    "Ніколи не було, і ось знову, рух у напрямку {region} 🟧",
]


def random_region() -> str:
    return random.choice(REGIONS)


def random_threat() -> str:
    return random.choice(THREATS)


def build_alert(region: str | None = None, threat: str | None = None) -> tuple[str, str, str]:
    region = region or random_region()
    threat = threat or random_threat()
    text = ALERT_TEMPLATE.replace("...", region)
    return text, region, threat


def build_clear(region: str) -> str:
    return CLEAR_TEMPLATE.replace("...", region)


def build_update(region: str | None = None) -> str:
    region = region or random_region()
    return random.choice(UPDATE_TEMPLATES).format(region=region)


async def send_alert(bot, channel_id):
    text, region, threat = build_alert()
    await bot.send_message(channel_id, text)
    await add_active_alert(region, threat)
    await log_post("alert", text)
    return region


async def send_clear(bot, channel_id, region: str | None = None):
    if region:
        await clear_alert_by_region(region)
    else:
        active = await pop_active_alert()
        region = active["region"] if active else random_region()
    text = build_clear(region)
    await bot.send_message(channel_id, text)
    await log_post("clear", text)
    return region


async def send_update(bot, channel_id, region: str | None = None):
    text = build_update(region)
    await bot.send_message(channel_id, text)
    await log_post("update", text)
