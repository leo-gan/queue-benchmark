from __future__ import annotations

import platform
import threading
from collections import deque
from typing import Any

from .base import QueueAdapter


class DequeLockQueue(QueueAdapter):
    name = "deque-lock"
    category = "locked"
    supports_mpmc = True
    communication = "thread"

    def version(self) -> str:
        return platform.python_version()

    def create(self, capacity: int | None = None) -> Any:
        return {"q": deque(), "lock": threading.Lock()}

    def enqueue(self, q: Any, item: bytes) -> None:
        with q["lock"]:
            q["q"].append(item)

    def dequeue(self, q: Any) -> bytes:
        while True:
            with q["lock"]:
                if q["q"]:
                    return q["q"].popleft()
