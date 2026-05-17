import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

DB_PATH = Path("bot_data.db")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(channel_id: str) -> None:
    with _connect() as db:
        db.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            is_paused INTEGER NOT NULL DEFAULT 0,
            channel_id TEXT NOT NULL
        )
        """)
        db.execute("""
        CREATE TABLE IF NOT EXISTS active_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            region TEXT NOT NULL,
            threat TEXT NOT NULL,
            started_at TEXT NOT NULL,
            clear_scheduled_at TEXT
        )
        """)
        db.execute("""
        CREATE TABLE IF NOT EXISTS post_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            text TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """)
        db.execute("INSERT OR IGNORE INTO settings (id, is_paused, channel_id) VALUES (1, 0, ?)", (channel_id,))
        db.execute("UPDATE settings SET channel_id = ? WHERE id = 1", (channel_id,))
        db.commit()


def is_paused() -> bool:
    with _connect() as db:
        row = db.execute("SELECT is_paused FROM settings WHERE id = 1").fetchone()
        return bool(row["is_paused"]) if row else False


def set_paused(value: bool) -> None:
    with _connect() as db:
        db.execute("UPDATE settings SET is_paused = ? WHERE id = 1", (1 if value else 0,))
        db.commit()


def add_active_alert(region: str, threat: str, clear_time: Optional[str] = None) -> int:
    with _connect() as db:
        cur = db.execute(
            "INSERT INTO active_alerts (region, threat, started_at, clear_scheduled_at) VALUES (?, ?, ?, ?)",
            (region, threat, datetime.utcnow().isoformat(), clear_time),
        )
        db.commit()
        return int(cur.lastrowid)


def get_random_active_alert() -> Optional[sqlite3.Row]:
    with _connect() as db:
        return db.execute("SELECT * FROM active_alerts ORDER BY RANDOM() LIMIT 1").fetchone()


def remove_active_alert(alert_id: int) -> None:
    with _connect() as db:
        db.execute("DELETE FROM active_alerts WHERE id = ?", (alert_id,))
        db.commit()


def count_active_alerts() -> int:
    with _connect() as db:
        row = db.execute("SELECT COUNT(*) AS c FROM active_alerts").fetchone()
        return int(row["c"])


def log_post(post_type: str, text: str) -> None:
    with _connect() as db:
        db.execute(
            "INSERT INTO post_logs (type, text, created_at) VALUES (?, ?, ?)",
            (post_type, text, datetime.utcnow().isoformat()),
        )
        db.commit()


def recent_texts(limit: int = 30) -> list[str]:
    with _connect() as db:
        rows = db.execute("SELECT text FROM post_logs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        return [r["text"] for r in rows]


def get_random_logged_text(types: tuple[str, ...] | None = None, limit: int = 200) -> str | None:
    with _connect() as db:
        if types:
            placeholders = ",".join("?" for _ in types)
            rows = db.execute(
                f"SELECT text FROM post_logs WHERE type IN ({placeholders}) ORDER BY id DESC LIMIT ?",
                (*types, limit),
            ).fetchall()
        else:
            rows = db.execute("SELECT text FROM post_logs ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
        if not rows:
            return None
        import random
        return random.choice(rows)["text"]
