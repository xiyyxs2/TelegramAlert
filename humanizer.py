import random

TAILS = [
    "поки так",
    "дивимось далі",
    "без паніки",
    "моніторинг триває",
    "оновлю, якщо буде щось нове",
    "на звʼязку",
    "коротко по ситуації",
    "працюємо",
    "при зміні напишу",
]

EMOJIS = ["🟧", "🟨", "📡", "🫡", "⚠️", ""]

BANNED_IN_POSTS = [
    "симуляційний канал",
    "не офіційне сповіщення",
    "не є офіційним",
    "це симуляція",
    "художній канал",
]


def ensure_dot(text: str) -> str:
    text = text.strip()
    if not text:
        return text
    if text[-1] not in ".!?…🟧🟨🟥":
        text += "."
    return text


def humanize_regular(text: str) -> str:
    text = text.strip()
    if random.random() < 0.25 and len(text) < 130:
        tail = random.choice(TAILS)
        text = f"{text}, {tail}"
    if random.random() < 0.22:
        emoji = random.choice(EMOJIS)
        if emoji and emoji not in text:
            text = f"{text} {emoji}"
    return ensure_dot(text)


def add_simulation_label(text: str, enabled: bool = False) -> str:
    # У постах каналу нічого не дописуємо. Попередження лишається тільки в README/описі каналу.
    cleaned = text.strip()
    lower = cleaned.lower()
    for banned in BANNED_IN_POSTS:
        if banned in lower:
            cleaned = cleaned.replace(banned, "").strip()
    return cleaned
