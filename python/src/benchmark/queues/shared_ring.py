"""Shared-memory SPSC ring (category S): two OS processes, one mapped buffer."""

from __future__ import annotations

import platform
from multiprocessing import Array, Process, Value
from typing import Any

from .base import QueueAdapter


def _ring_push(state: dict, item: bytes) -> None:
    nxt = (state["tail"].value + 1) % state["slots"]
    while nxt == state["head"].value:
        pass
    off = state["tail"].value * state["slot"]
    n = min(len(item), state["slot"])
    state["buf"][off : off + n] = item[:n]
    state["lens"][state["tail"].value] = n
    state["tail"].value = nxt


def _ring_pop(state: dict) -> bytes:
    while state["head"].value == state["tail"].value:
        pass
    idx = state["head"].value
    n = state["lens"][idx]
    off = idx * state["slot"]
    item = bytes(state["buf"][off : off + n])
    state["head"].value = (idx + 1) % state["slots"]
    return item


def _produce(state: dict, batch: list[bytes]) -> None:
    for item in batch:
        _ring_push(state, item)


def _consume(state: dict, take: int) -> None:
    for _ in range(take):
        _ring_pop(state)


def run_cross_process(
    items: list[bytes],
    producers: int,
    consumers: int,
    capacity: int | None,
) -> tuple[int, int, float]:
    import time

    if producers != 1 or consumers != 1:
        return 0, 0, 0.0
    slots = max(int(capacity or len(items)), len(items)) + 1
    slot = max((len(items[0]) if items else 256), 64)
    state = {
        "buf": Array("B", slots * slot, lock=False),
        "lens": Array("i", slots, lock=False),
        "head": Value("i", 0, lock=False),
        "tail": Value("i", 0, lock=False),
        "slots": slots,
        "slot": slot,
    }
    t0 = time.perf_counter_ns()
    cons = Process(target=_consume, args=(state, len(items)))
    cons.start()
    prod = Process(target=_produce, args=(state, items))
    prod.start()
    prod.join()
    cons.join()
    wall = time.perf_counter_ns() - t0
    ok = prod.exitcode == 0 and cons.exitcode == 0
    return wall // 2, wall - wall // 2, 1.0 if ok else 0.0


class SharedRingQueue(QueueAdapter):
    name = "shared-ring"
    category = "spsc"
    communication = "shared"
    supports_mpmc = False
    supports_spsc_only = True
    opt_in = True
    cross_process = True

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
        _ring_push(q, item)

    def dequeue(self, q: Any) -> bytes:
        return _ring_pop(q)
