"""stdlib queue.SimpleQueue: unbounded C-accelerated threading MPMC."""

from __future__ import annotations

import platform
import queue
from typing import Any

from .base import QueueAdapter


class SimpleQueueAdapter(QueueAdapter):
    name = "queue.SimpleQueue"
    category = "concurrent"
    supports_mpmc = True
    supports_bounded = False
    communication = "thread"

    def version(self) -> str:
        return platform.python_version()

    def create(self, capacity: int | None = None) -> Any:
        # SimpleQueue is unbounded; capacity is ignored (supports_bounded=False).
        return queue.SimpleQueue()

    def enqueue(self, q: Any, item: bytes) -> None:
        q.put(item)

    def dequeue(self, q: Any) -> bytes:
        return q.get()
