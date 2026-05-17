import random
import aiohttp
from config import config
from alerts import random_region
from database import log_post

WEATHER_STARTS = [
    "🌤️ Коротко по погоді в {city}:",
    "Утренній апдейт по погоді, {city}:",
    "По погоді на сьогодні, {city}:",
    "☁️ {city}, прогноз на зараз:",
    "Погодний моніторинг, {city}:",
]

FAKE_WEATHER = [
    "температура близько {temp}°C, вітер {wind} м/с, хмарність {clouds}%.",
    "приблизно {temp}°C, вітер до {wind} м/с. Загалом терпимо.",
    "{temp}°C, хмарність {clouds}%, по опадах без чіткої картини.",
    "погода рівна: {temp}°C, вітер {wind} м/с.",
]


def _fake_weather(city: str) -> str:
    return random.choice(WEATHER_STARTS).format(city=city) + " " + random.choice(FAKE_WEATHER).format(
        temp=random.randint(-5, 34),
        wind=random.randint(1, 12),
        clouds=random.randint(0, 100),
    )


async def fetch_weather(city: str) -> str:
    if not config.OPENWEATHER_API_KEY:
        return _fake_weather(city)

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": config.OPENWEATHER_API_KEY,
        "units": "metric",
        "lang": "ua",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, timeout=10) as resp:
                if resp.status != 200:
                    return _fake_weather(city)
                data = await resp.json()
        temp = round(data["main"]["temp"])
        wind = data.get("wind", {}).get("speed", 0)
        clouds = data.get("clouds", {}).get("all", 0)
        desc = data.get("weather", [{}])[0].get("description", "без опису")
        return random.choice(WEATHER_STARTS).format(city=city) + f" {temp}°C, вітер {wind} м/с, хмарність {clouds}%, {desc}."
    except Exception:
        return _fake_weather(city)


async def send_weather(bot, channel_id):
    city = random.choice([config.DEFAULT_CITY, random_region(), "Київ", "Одеса", "Львів", "Каїр", "Варшава", "Берлін", "Токіо"])
    text = await fetch_weather(city)
    await bot.send_message(channel_id, text)
    await log_post("weather", text)
