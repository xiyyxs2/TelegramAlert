import aiosqlite
from datetime import datetime
from config import config


async def init_db():
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            is_paused INTEGER NOT NULL DEFAULT 0,
            channel_id TEXT
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS active_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT NOT NULL,
            threat TEXT,
            started_at TEXT NOT NULL,
            clear_scheduled_at TEXT
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS post_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)
        await db.execute("""
        CREATE TABLE IF NOT EXISTS runtime_stats (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)
        await db.execute(
            "INSERT OR IGNORE INTO settings (id, is_paused, channel_id) VALUES (1, 0, ?)",
            (config.CHANNEL_ID,),
        )
        await db.commit()


async def is_paused() -> bool:
    async with aiosqlite.connect(config.DB_PATH) as db:
        cur = await db.execute("SELECT is_paused FROM settings WHERE id = 1")
        row = await cur.fetchone()
        return bool(row[0]) if row else False


async def set_paused(value: bool):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute("UPDATE settings SET is_paused = ? WHERE id = 1", (1 if value else 0,))
        await db.commit()


async def log_post(post_type: str, text: str):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            "INSERT INTO post_logs (type, text, created_at) VALUES (?, ?, ?)",
            (post_type, text, datetime.utcnow().isoformat()),
        )
        await db.commit()


async def get_recent_posts(limit: int = 30):
    async with aiosqlite.connect(config.DB_PATH) as db:
        cur = await db.execute(
            "SELECT text FROM post_logs ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = await cur.fetchall()
        return [r[0] for r in rows]


async def add_active_alert(region: str, threat: str, clear_scheduled_at: str | None = None):
    async with aiosqlite.connect(config.DB_PATH) as db:
        cur = await db.execute(
            "INSERT INTO active_alerts (region, threat, started_at, clear_scheduled_at) VALUES (?, ?, ?, ?)",
            (region, threat, datetime.utcnow().isoformat(), clear_scheduled_at),
        )
        await db.commit()
        return cur.lastrowid


async def get_active_alerts():
    async with aiosqlite.connect(config.DB_PATH) as db:
        cur = await db.execute("SELECT id, region, threat, started_at FROM active_alerts ORDER BY id ASC")
        rows = await cur.fetchall()
        return [{"id": r[0], "region": r[1], "threat": r[2], "started_at": r[3]} for r in rows]


async def pop_active_alert():
    alerts = await get_active_alerts()
    if not alerts:
        return None
    alert = alerts[0]
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute("DELETE FROM active_alerts WHERE id = ?", (alert["id"],))
        await db.commit()
    return alert


async def clear_alert_by_region(region: str):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute("DELETE FROM active_alerts WHERE region = ?", (region,))
        await db.commit()


async def count_today_posts():
    today = datetime.utcnow().date().isoformat()
    async with aiosqlite.connect(config.DB_PATH) as db:
        cur = await db.execute("SELECT COUNT(*) FROM post_logs WHERE created_at LIKE ?", (f"{today}%",))
        row = await cur.fetchone()
        return row[0] if row else 0


async def set_stat(key: str, value: str):
    async with aiosqlite.connect(config.DB_PATH) as db:
        await db.execute(
            "INSERT INTO runtime_stats (key, value) VALUES (?, ?) ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )
        await db.commit()


async def get_stat(key: str, default: str = ""):
    async with aiosqlite.connect(config.DB_PATH) as db:
        cur = await db.execute("SELECT value FROM runtime_stats WHERE key = ?", (key,))
        row = await cur.fetchone()
        return row[0] if row else default
