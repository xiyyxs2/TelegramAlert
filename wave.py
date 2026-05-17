import random
from humanizer import add_simulation_label
from alerts import random_region

WAVE_TEMPLATES = [
    "🌊 Зафіксована енергетична хвиля.\nІнтенсивність: {percent}%\nДжерело: {region}.",
    "🌊 По моніторингу проходить хвиля.\nСила: {percent}%\nЙмовірне джерело: {region}.",
    "🌀 Дивна хвиля пішла з боку {region}.\nІнтенсивність приблизно {percent}%.",
    "🌫️ Фон трохи поплив.\nРегіон: {region}\nІнтенсивність: {percent}%.",
]


def make_wave(simulation_label: bool = True) -> str:
    return add_simulation_label(
        random.choice(WAVE_TEMPLATES).format(percent=random.randint(10, 100), region=random_region()),
        simulation_label,
    )
