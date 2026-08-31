"""SPSC ring: one producer, one consumer, no mutex on the happy path."""

from __future__ import annotations

import platform
from typing import Any

from .base import QueueAdapter


class SpscRingQueue(QueueAdapter):
    name = "spsc-ring"
    category = "spsc"
    supports_mpmc = False
    supports_spsc_only = True
    communication = "thread"

    def version(self) -> str:
        return platform.python_version()

    def create(self, capacity: int | None = None) -> Any:
        n = max(int(capacity or 8), 8)
        # One extra slot so head==tail means empty.
        cap = n + 1
        return {"buf": [None] * cap, "cap": cap, "head": 0, "tail": 0}

    def enqueue(self, q: Any, item: bytes) -> None:
        nxt = (q["tail"] + 1) % q["cap"]
        if nxt == q["head"]:
            raise RuntimeError("spsc-ring full")
        q["buf"][q["tail"]] = item
        q["tail"] = nxt

    def dequeue(self, q: Any) -> bytes:
        if q["head"] == q["tail"]:
            raise RuntimeError("spsc-ring empty")
        item = q["buf"][q["head"]]
        q["head"] = (q["head"] + 1) % q["cap"]
        return item
