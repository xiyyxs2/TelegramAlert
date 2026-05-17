# Telegram Sim Alert Bot — flat version

Симуляционный Telegram-бот для игрового/художественного канала. Все сообщения вымышленные. Это не официальный источник оповещений.

Эта версия сделана специально для телефона: **без папок вообще**. Все файлы лежат в корне репозитория, поэтому их можно загрузить в GitHub обычной загрузкой файлов.

## Файлы

```text
main.py
config.py
database.py
scheduler.py
weather.py
humanizer.py
admin.py
alerts.py
random_posts.py
wave.py
requirements.txt
.env.example
.gitignore
Procfile
runtime.txt
README.md
```

## Команды

```text
/start
/status
/pause
/resume
/test_post
/test_alert
/test_clear
/test_wave
/test_weather
```

Канал бот ведёт сам. Команды нужны только для контроля и теста.

## ENV для Railway

Добавь в Railway → Variables:

```env
BOT_TOKEN=PASTE_NEW_BOT_TOKEN_HERE
ADMIN_ID=123456789
CHANNEL_ID=-1001234567890
OPENWEATHER_API_KEY=
TIMEZONE=Europe/Kyiv
MIN_POSTS_PER_DAY=15
MAX_POSTS_PER_DAY=45
SIMULATION_LABEL=true
```

`SIMULATION_LABEL=true` добавляет к постам пометку, что это симуляция.

## Как загрузить в GitHub с телефона

1. Скачай ZIP.
2. Распакуй его в приложении «Файлы».
3. Открой GitHub → свой репозиторий.
4. Нажми `Add file` → `Upload files`.
5. Выдели **все файлы внутри папки**, не саму папку.
6. Загрузи файлы.
7. Нажми `Commit changes`.

Важно: в репозитории сразу должны лежать `main.py`, `requirements.txt`, `Procfile`, а не папка внутри папки.

## Railway

1. Railway → New Project.
2. Deploy from GitHub repo.
3. Выбери репозиторий.
4. Добавь Variables.
5. Нажми Redeploy.

Procfile уже настроен:

```text
worker: python main.py
```

## Telegram-канал

1. Добавь бота в канал.
2. Сделай его администратором.
3. Дай право публиковать сообщения.
4. В `CHANNEL_ID` укажи ID канала вида `-100...`.

## Если токен попал в чат/GitHub

1. Открой @BotFather.
2. `/mybots`.
3. Выбери бота.
4. API Token.
5. Revoke current token.
6. Новый токен вставь в Railway Variables.
