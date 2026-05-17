import random
import re

ENDINGS = [
    "",
    "",
    "",
    " Працюємо.",
    " Моніторинг триває.",
    " При змінах оновимо.",
    " Без зайвої паніки.",
]

EMOJIS = ["", "", "", "🟨", "🟧", "📡", "🛰️", "⚠️", "📍"]

FORBIDDEN_IN_POSTS = [
    "симуляційний канал",
    "не офіційне сповіщення",
    "не є офіційним джерелом",
    "це симуляція",
    "художній канал",
    "fictional",
    "simulation",
]


def clean_text(text: str) -> str:
    text = re.sub(r"\n{3,}", "\n\n", text.strip())
    for bad in FORBIDDEN_IN_POSTS:
        text = text.replace(bad, "").replace(bad.capitalize(), "")
    return text.strip()


def ensure_sentence(text: str) -> str:
    text = clean_text(text)
    if not text:
        return "Моніторинг триває."
    if text.endswith((".", "!", "?", "…", "🟨", "🟧", "🟥", "✅")):
        return text
    return text + "."


def humanize_regular(text: str) -> str:
    text = ensure_sentence(text)
    if random.randint(1, 100) <= 22:
        text += random.choice(ENDINGS)
    if random.randint(1, 100) <= 25:
        emoji = random.choice(EMOJIS)
        if emoji and emoji not in text:
            text = f"{text} {emoji}"
    return clean_text(text)


def humanize_blog(text: str) -> str:
    text = clean_text(text)
    if len(text) > 450:
        text = text[:430].rsplit(" ", 1)[0] + "."
    return ensure_sentence(text)


def prepare_message(text: str, post_type: str = "regular") -> str:
    if post_type in {"alert", "clear"}:
        return clean_text(text)
    if post_type == "blog":
        return humanize_blog(text)
    return humanize_regular(text)
