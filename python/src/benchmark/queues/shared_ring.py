"""Shared-memory SPSC ring (category S). Same process maps one buffer."""

from __future__ import annotations

import platform
from multiprocessing import Array, Value
from typing import Any

from .base import QueueAdapter


class SharedRingQueue(QueueAdapter):
    name = "shared-ring"
    category = "spsc"
    communication = "shared"
    supports_mpmc = False
    supports_spsc_only = True
    opt_in = True

    def version(self) -> str:
        return platform.python_version()

    def create(self, capacity: int | None = None) -> Any:
        slots = max(int(capacity or 8), 8) + 1
        slot = 4096
        return {
            "buf": Array("B", slots * slot, lock=False),
            "lens": Array("i", slots, lock=False),
            "head": Value("i", 0, lock=False),
            "tail": Value("i", 0, lock=False),
            "slots": slots,
            "slot": slot,
        }

    def enqueue(self, q: Any, item: bytes) -> None:
        nxt = (q["tail"].value + 1) % q["slots"]
        while nxt == q["head"].value:
            pass
        off = q["tail"].value * q["slot"]
        n = min(len(item), q["slot"])
        q["buf"][off : off + n] = item[:n]
        q["lens"][q["tail"].value] = n
        q["tail"].value = nxt

    def dequeue(self, q: Any) -> bytes:
        while q["head"].value == q["tail"].value:
            pass
        idx = q["head"].value
        n = q["lens"][idx]
        off = idx * q["slot"]
        item = bytes(q["buf"][off : off + n])
        q["head"].value = (idx + 1) % q["slots"]
        return item
