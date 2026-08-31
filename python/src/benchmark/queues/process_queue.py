"""Process / IPC queue (category P)."""

from __future__ import annotations

import platform
from multiprocessing import Queue
from typing import Any

from .base import QueueAdapter


class ProcessQueue(QueueAdapter):
    name = "multiprocessing.Queue"
    category = "concurrent"
    communication = "process"
    supports_mpmc = True
    opt_in = True

    def version(self) -> str:
        return platform.python_version()

    def create(self, capacity: int | None = None) -> Any:
        return Queue(maxsize=int(capacity) if capacity else 0)

    def enqueue(self, q: Any, item: bytes) -> None:
        q.put(item)

    def dequeue(self, q: Any) -> bytes:
        return q.get()
