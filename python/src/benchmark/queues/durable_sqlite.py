"""Local sqlite queue (category D)."""

from __future__ import annotations

import os
import platform
import sqlite3
import tempfile
from typing import Any

from .base import QueueAdapter


class DurableSqliteQueue(QueueAdapter):
    name = "sqlite-queue"
    category = "durable"
    communication = "durable"
    supports_mpmc = False
    supports_spsc_only = True
    opt_in = True

    def version(self) -> str:
        return platform.python_version()

    def create(self, capacity: int | None = None) -> Any:
        fd, path = tempfile.mkstemp(prefix="qb-durable-", suffix=".sqlite")
        os.close(fd)
        conn = sqlite3.connect(path, isolation_level=None)
        durable = os.environ.get("BENCHMARK_FSYNC", "").strip() in {"1", "true", "on"}
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=FULL" if durable else "PRAGMA synchronous=OFF")
        conn.execute("CREATE TABLE q (id INTEGER PRIMARY KEY, payload BLOB)")
        return {"conn": conn, "path": path, "durable": durable}

    def enqueue(self, q: Any, item: bytes) -> None:
        q["conn"].execute("INSERT INTO q(payload) VALUES (?)", (item,))

    def dequeue(self, q: Any) -> bytes:
        cur = q["conn"].execute("SELECT id, payload FROM q ORDER BY id LIMIT 1")
        row = cur.fetchone()
        if row is None:
            raise RuntimeError("sqlite-queue empty")
        q["conn"].execute("DELETE FROM q WHERE id=?", (row[0],))
        return row[1]
