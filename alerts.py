import random
from datetime import datetime, timedelta
import database
from humanizer import add_simulation_label, humanize_regular

ALERT_TEMPLATE = """🔴 ... - повітряна тривога!\n\n😇Підпишись. Повітряна тривога - Світ. Працює 24/7.\n📡 Куди летить? Завжди на звязку! Моніторинг | Радар📍🔫"""
CLEAR_TEMPLATE = """🟢... - відбій повітряної тривоги!\n\n😇Підпишись. Повітряна тривога - Світ. Працює 24/7.\n📡 Куди летить? Завжди на звязку! Моніторинг | Радар📍🔫"""

COUNTRIES = [
    "Україна", "Польща", "Німеччина", "Франція", "Італія", "Іспанія", "Португалія", "Румунія", "Молдова", "Чехія", "Словаччина", "Угорщина", "Австрія", "Швейцарія", "Нідерланди", "Бельгія", "Данія", "Швеція", "Норвегія", "Фінляндія", "Ісландія", "Ірландія", "Велика Британія", "Естонія", "Латвія", "Литва", "Білорусь", "Грузія", "Вірменія", "Азербайджан", "Туреччина", "Греція", "Болгарія", "Сербія", "Хорватія", "Словенія", "Боснія і Герцеговина", "Чорногорія", "Албанія", "Північна Македонія", "Косово",
    "США", "Канада", "Мексика", "Бразилія", "Аргентина", "Чилі", "Перу", "Колумбія", "Венесуела", "Еквадор", "Болівія", "Парагвай", "Уругвай", "Куба", "Ямайка", "Панама", "Коста-Рика",
    "Китай", "Японія", "Південна Корея", "Північна Корея", "Індія", "Пакистан", "Бангладеш", "Індонезія", "Філіппіни", "Вʼєтнам", "Таїланд", "Малайзія", "Сінгапур", "Монголія", "Казахстан", "Узбекистан", "Киргизстан", "Таджикистан", "Туркменістан", "Афганістан", "Іран", "Ірак", "Сирія", "Ізраїль", "Йорданія", "Ліван", "Саудівська Аравія", "ОАЕ", "Катар", "Кувейт", "Оман", "Ємен",
    "Єгипет", "Марокко", "Алжир", "Туніс", "Лівія", "Судан", "Ефіопія", "Кенія", "Танзанія", "Уганда", "Руанда", "Нігерія", "Гана", "Камерун", "Сенегал", "ПАР", "Мадагаскар",
    "Австралія", "Нова Зеландія", "Фіджі", "Папуа Нова Гвінея"
]

CITIES = [
    "Київ", "Львів", "Одеса", "Харків", "Дніпро", "Запоріжжя", "Варшава", "Краків", "Берлін", "Париж", "Лондон", "Рим", "Мадрид", "Прага", "Відень", "Амстердам", "Стокгольм", "Осло", "Токіо", "Сеул", "Пекін", "Шанхай", "Сінгапур", "Дубай", "Каїр", "Нью-Йорк", "Лос-Анджелес", "Торонто", "Мехіко", "Буенос-Айрес", "Ріо-де-Жанейро", "Сідней"
]

FANTASY_REGIONS = [
    "Пушенленд", "Пошона", "Луна", "Марс", "Галактика 69", "Сектор Омега", "Внешний пояс колоний", "Внутренний купол", "Зона 404", "Північний кратер", "Південна башта", "Старий радар", "Туманний сектор", "Архівний пояс", "Сектор Нуль", "Портал 12", "Зелений коридор", "Чорний маяк"
]

THREATS = [
    "крылатая ракета", "баллистическая ракета", "гиперзвуковая ракета", "рой дронов", "ударные БПЛА", "шахед-дроны", "разведывательные БПЛА", "ракетный удар", "массированный ракетный обстрел", "воздушная угроза", "неизвестный летательный объект", "дивний сигнал", "радарна аномалія", "невідомий шум у секторі"
]

UPDATES = [
    "Є оновлення по {region}: фіксується {threat}.",
    "По {region} ситуація мутна, але моніторинг триває.",
    "Радар біля {region} бачить якусь активність. Поки уточнюємо.",
    "{region}: є підозрілий рух, без зайвої паніки.",
    "Карта біля {region} знову живе своїм життям.",
    "Супутник щось зловив у напрямку {region}, дивимось далі.",
]

ODD_MESSAGES = [
    "Радар зафіксував дивний рух у напрямку {region}",
    "Супутник щось побачив біля {region}, але зробив вигляд, що не бачив",
    "У {region} помічено нестабільний фон",
    "{region}: ситуація дивна, але контрольована",
    "На карті біля {region} зʼявилась підозріла активність",
    "Невелике викривлення сигналу біля {region}",
    "Моніторинг показує шум у секторі: {region}",
    "Є відчуття, що {region} сьогодні буде в новинах",
    "Сигнал з {region} нестабільний",
    "Напрямок незрозумілий, але радар нервує",
]


def random_region() -> str:
    return random.choice(COUNTRIES + CITIES + FANTASY_REGIONS)


def random_threat() -> str:
    return random.choice(THREATS)


def make_alert(simulation_label: bool = True) -> tuple[str, str, str]:
    region = random_region()
    threat = random_threat()
    text = ALERT_TEMPLATE.replace("...", region)
    return region, threat, add_simulation_label(text, simulation_label)


def make_clear(region: str, simulation_label: bool = True) -> str:
    text = CLEAR_TEMPLATE.replace("...", region)
    return add_simulation_label(text, simulation_label)


def make_update(simulation_label: bool = True) -> str:
    row = database.get_random_active_alert()
    region = row["region"] if row else random_region()
    threat = row["threat"] if row else random_threat()
    text = random.choice(UPDATES).format(region=region, threat=threat)
    return add_simulation_label(humanize_regular(text), simulation_label)


def make_odd_message(simulation_label: bool = True) -> str:
    text = random.choice(ODD_MESSAGES).format(region=random_region())
    return add_simulation_label(humanize_regular(text), simulation_label)


def start_alert_in_db(region: str, threat: str) -> int:
    clear_time = (datetime.utcnow() + timedelta(minutes=random.randint(15, 120))).isoformat()
    return database.add_active_alert(region, threat, clear_time)


def pop_random_alert() -> tuple[int, str] | None:
    row = database.get_random_active_alert()
    if not row:
        return None
    database.remove_active_alert(int(row["id"]))
    return int(row["id"]), row["region"]
