from __future__ import annotations

import platform
import queue
from typing import Any

from .base import QueueAdapter


class StdlibQueue(QueueAdapter):
    name = "queue.Queue"
    category = "concurrent"
    supports_mpmc = True

    def version(self) -> str:
        return platform.python_version()

    def create(self, capacity: int | None = None) -> Any:
        return queue.Queue()

    def enqueue(self, q: Any, item: bytes) -> None:
        q.put(item)

    def dequeue(self, q: Any) -> bytes:
        return q.get()
