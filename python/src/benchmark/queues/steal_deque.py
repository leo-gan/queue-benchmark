"""Chase-Lev style work-stealing deque (owner uses one end, thieves the other)."""

from __future__ import annotations

import platform
import threading
from collections import deque
from typing import Any

from .base import QueueAdapter


class StealDequeQueue(QueueAdapter):
    name = "steal-deque"
    category = "work-stealing"
    communication = "thread"
    supports_mpmc = True

    def version(self) -> str:
        return platform.python_version()

    def create(self, capacity: int | None = None) -> Any:
        return {"q": deque(), "lock": threading.Lock()}

    def enqueue(self, q: Any, item: bytes) -> None:
        # Owner push (bottom).
        with q["lock"]:
            q["q"].append(item)

    def dequeue(self, q: Any) -> bytes:
        # Thieves steal from the top (left). Owner-local pop is the right end.
        while True:
            with q["lock"]:
                if q["q"]:
                    return q["q"].popleft()
