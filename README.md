# Telegram Sim Alert Bot

Автопостер для Telegram-канала. Бот сам публикует тревоги, отбои, обновления, блоговые сообщения, волны и погоду.

## Важно

Проект предназначен для художественного / симуляционного канала. Не выдавайте канал за официальный источник информации.

Бот не дописывает предупреждение в каждый пост, чтобы сообщения выглядели чисто. Лучше указать формат канала в описании или закрепе.

## Файлы

Все файлы лежат в корне, без папок, чтобы их было удобно загрузить в GitHub с телефона.

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

## Railway Variables

Добавьте в Railway → Variables:

```env
BOT_TOKEN=новый_токен_бота
ADMIN_ID=ваш_telegram_id
CHANNEL_ID=-100xxxxxxxxxx
OPENWEATHER_API_KEY=
TIMEZONE=Europe/Kyiv
DEFAULT_CITY=Київ
MIN_POSTS_PER_DAY=15
MAX_POSTS_PER_DAY=45
REPEAT_OLD_POST_CHANCE=18
```

`OPENWEATHER_API_KEY` можно оставить пустым. Тогда погода будет генерироваться автоматически.

## Команды

Команды работают только для ADMIN_ID:

```text
/start
/status
/pause
/resume
/test_post
/test_blog
/test_alert
/test_clear
/test_update
/test_wave
/test_weather
```

## Как загрузить с телефона в GitHub

1. Скачайте ZIP.
2. Распакуйте.
3. Откройте папку `telegram_sim_alert_bot_full`.
4. В GitHub создайте private repository.
5. Нажмите `Add file` → `Upload files`.
6. Загружайте файлы из папки, не саму папку.
7. В репозитории в корне должны лежать `main.py`, `requirements.txt`, `Procfile`, `runtime.txt`.
8. Нажмите `Commit changes`.

Не загружайте `.env`. В GitHub должен быть только `.env.example`.

## Railway

1. Создайте Railway project.
2. Выберите `Deploy from GitHub repo`.
3. Подключите репозиторий.
4. Добавьте Variables.
5. Нажмите Redeploy.

Procfile уже готов:

```text
worker: python main.py
```

## Telegram channel

1. Создайте канал.
2. Добавьте бота в администраторы.
3. Дайте право публиковать сообщения.
4. Укажите `CHANNEL_ID` в Railway Variables.

Для публичного канала можно попробовать `CHANNEL_ID=@channel_username`, но лучше использовать числовой ID вида `-100...`.

## Если бот не пишет

Проверьте:

1. Бот добавлен админом в канал.
2. У бота есть право Post Messages.
3. `CHANNEL_ID` правильный.
4. `BOT_TOKEN` правильный и новый.
5. После изменения Variables был Redeploy.
