import random

SOFT_ENDINGS = [
    "поки так", "дивимось далі", "без паніки", "моніторинг триває",
    "на звʼязку", "коротко по ситуації", "карта сьогодні дивна", "радар трохи чудить",
]
PREFIXES = ["", "Коротко: ", "Апдейт: ", "По моніторингу: ", "Так, дивіться: "]
EMOJIS = ["📡", "🛰️", "📍", "🌫️", "🧭", "🔭", "⚠️", "🌊"]


def ensure_dot(text: str) -> str:
    text = text.strip()
    if not text:
        return "."
    if text[-1] not in ".!?…":
        text += "."
    return text


def humanize_regular(text: str) -> str:
    text = text.strip()
    if random.random() < 0.25:
        text = random.choice(PREFIXES) + text[:1].lower() + text[1:]
    if random.random() < 0.25:
        text = f"{random.choice(EMOJIS)} {text}"
    if random.random() < 0.35:
        text = f"{text.rstrip('.!?…')}, {random.choice(SOFT_ENDINGS)}"
    return ensure_dot(text)


def add_simulation_label(text: str, enabled: bool) -> str:
    if not enabled:
        return text
    label = "\n\nСимуляційний канал. Не офіційне сповіщення."
    return text + label
