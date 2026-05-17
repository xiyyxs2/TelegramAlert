import random
from humanizer import add_simulation_label
from alerts import random_region

WAVES = [
    "🌊 Зафіксована енергетична хвиля.\nІнтенсивність: {percent}%\nДжерело: {region}.",
    "🌊 По моніторингу проходить хвиля.\nСила: {percent}%\nЙмовірне джерело: {region}.",
    "🌀 Дивна хвиля пішла з боку {region}.\nІнтенсивність приблизно {percent}%.",
    "🌊 Короткий сигнал хвилі.\n{region}, інтенсивність {percent}%.",
    "🟧 Хвиля по напрямку {region}.\nПоказник: {percent}%.",
]


def make_wave(simulation_label: bool = True) -> str:
    text = random.choice(WAVES).format(percent=random.randint(10, 100), region=random_region())
    return add_simulation_label(text, simulation_label)
