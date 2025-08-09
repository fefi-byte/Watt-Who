from __future__ import annotations

import sqlite3
from pathlib import Path

from .models import Event


class Storage:
    """Persistenz in SQLite."""

    def __init__(self, db_path: str | Path = "nilm.db") -> None:
        self.conn = sqlite3.connect(str(db_path))
        self._init_db()

    def _init_db(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                delta_w REAL,
                duration_s REAL,
                device TEXT,
                confidence REAL
            )
            """
        )
        self.conn.commit()

    def insert_event(self, event: Event) -> int:
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO events (timestamp, delta_w, duration_s, device, confidence) VALUES (?, ?, ?, ?, ?)",
            (
                event.timestamp,
                event.delta_w,
                event.duration_s,
                getattr(event, "device_id", None),
                event.confidence,
            ),
        )
        self.conn.commit()
        return int(cur.lastrowid or 0)
