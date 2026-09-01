"""Process / IPC SimpleQueue (category P): unbounded pipe, no maxsize."""

from __future__ import annotations

import platform
from multiprocessing import SimpleQueue
from typing import Any

from . import process_queue
from .base import QueueAdapter


def _make(_capacity: int | None) -> Any:
    return SimpleQueue()


def run_cross_process(
    items: list[bytes],
    producers: int,
    consumers: int,
    capacity: int | None,
) -> tuple[int, int, float]:
    return process_queue.run_cross_process(
        items, producers, consumers, capacity, make_queue=_make
    )


class ProcessSimpleQueue(QueueAdapter):
    name = "multiprocessing.SimpleQueue"
    category = "concurrent"
    communication = "process"
    supports_mpmc = True
    supports_bounded = False
    opt_in = True
    cross_process = True
    run_cross_process = staticmethod(run_cross_process)

    def version(self) -> str:
        return platform.python_version()

    def create(self, capacity: int | None = None) -> Any:
        return SimpleQueue()

    def enqueue(self, q: Any, item: bytes) -> None:
        q.put(item)

    def dequeue(self, q: Any) -> bytes:
        return q.get()
