"""Process / IPC queue (category P): two or more OS processes, pickle over a pipe."""

from __future__ import annotations

import platform
from multiprocessing import Process, Queue
from typing import Any

from .base import QueueAdapter


def _produce(q: Queue, batch: list[bytes]) -> None:
    for item in batch:
        q.put(item)


def _consume(q: Queue, take: int) -> None:
    for _ in range(take):
        q.get()


def run_cross_process(
    items: list[bytes],
    producers: int,
    consumers: int,
    capacity: int | None,
    make_queue: Any | None = None,
) -> tuple[int, int, float]:
    """Time a real multi-process handoff. Returns (enq_ns, deq_ns, fidelity)."""
    import time

    if make_queue is None:
        q: Any = Queue(maxsize=int(capacity) if capacity else 0)
    else:
        q = make_queue(capacity)
    n = len(items)
    producers = max(1, producers)
    consumers = max(1, consumers)
    batches = []
    start = 0
    for i in range(producers):
        end = n * (i + 1) // producers
        batches.append(items[start:end])
        start = end
    per = n // consumers
    extra = n % consumers
    procs: list[Process] = []
    t0 = time.perf_counter_ns()
    for batch in batches:
        p = Process(target=_produce, args=(q, batch))
        p.start()
        procs.append(p)
    for i in range(consumers):
        take = per + (extra if i == 0 else 0)
        p = Process(target=_consume, args=(q, take))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()
    wall = time.perf_counter_ns() - t0
    ok = all(p.exitcode == 0 for p in procs)
    return wall // 2, wall - wall // 2, 1.0 if ok else 0.0


class ProcessQueue(QueueAdapter):
    name = "multiprocessing.Queue"
    category = "concurrent"
    communication = "process"
    supports_mpmc = True
    opt_in = True
    cross_process = True

    def version(self) -> str:
        return platform.python_version()

    def create(self, capacity: int | None = None) -> Any:
        return Queue(maxsize=int(capacity) if capacity else 0)

    def enqueue(self, q: Any, item: bytes) -> None:
        q.put(item)

    def dequeue(self, q: Any) -> bytes:
        return q.get()
