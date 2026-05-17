import random
import aiohttp
from humanizer import add_simulation_label
from alerts import CITIES, COUNTRIES, FANTASY_REGIONS, random_region

WEATHER_STARTS = [
    "🌤️ Погода по {region}:",
    "Коротко по погоді в {region}:",
    "Ранковий прогноз для {region}:",
    "По {region} на сьогодні:",
    "☁️ Метеоапдейт, {region}:",
]

SIM_WEATHER_ENDS = [
    "загалом терпимо", "радар каже, що жити можна", "атмосфера дивна, але нормальна", "небо сьогодні щось задумало", "без особливої драми"
]


def _weather_region() -> str:
    return random.choice(CITIES + COUNTRIES + FANTASY_REGIONS)


async def get_weather_text(api_key: str, simulation_label: bool = True) -> str:
    region = _weather_region()
    if api_key and region in CITIES:
        try:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"q": region, "appid": api_key, "units": "metric", "lang": "ua"}
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params, timeout=10) as response:
                    data = await response.json()
            if "main" in data:
                temp = round(data["main"].get("temp", 0))
                wind = data.get("wind", {}).get("speed", 0)
                clouds = data.get("clouds", {}).get("all", 0)
                desc = data.get("weather", [{}])[0].get("description", "без опису")
                text = f"{random.choice(WEATHER_STARTS).format(region=region)} {temp}°C, вітер {wind} м/с, хмарність {clouds}%, {desc}."
                return add_simulation_label(text, simulation_label)
        except Exception:
            pass

    temp = random.randint(-5, 34)
    wind = round(random.uniform(0.5, 12.0), 1)
    clouds = random.randint(0, 100)
    text = f"{random.choice(WEATHER_STARTS).format(region=region)} приблизно {temp}°C, вітер {wind} м/с, хмарність {clouds}%, {random.choice(SIM_WEATHER_ENDS)}."
    return add_simulation_label(text, simulation_label)
