"""Map CSV io_mode / env overrides to a producer×consumer pattern."""

from __future__ import annotations

import os
import re

_ALIASES = {
    "bytes": (1, 1),
    "string": (1, 1),
    "spsc": (1, 1),
    "stream": (2, 2),
    "mpmc": (2, 2),
}

_PXC = re.compile(r"^(\d+)p(\d+)c$")


def parse_pattern(io_mode: str) -> tuple[int, int]:
    raw = (io_mode or "bytes").strip().lower()
    if raw in _ALIASES:
        return _ALIASES[raw]
    m = _PXC.match(raw)
    if m:
        return max(1, int(m.group(1))), max(1, int(m.group(2)))
    return 1, 1


def env_bound() -> int | None:
    v = os.environ.get("BENCHMARK_BOUND", "").strip()
    if not v:
        return None
    n = int(v)
    return n if n > 0 else None


def env_slow_consumer_ns() -> int:
    v = os.environ.get("BENCHMARK_SLOW_CONSUMER_NS", "").strip()
    return int(v) if v else 0


def env_special() -> str:
    """wakeup | burst | cancel | ''."""
    return (os.environ.get("BENCHMARK_SPECIAL") or "").strip().lower()


def env_wait_ns() -> int:
    v = os.environ.get("BENCHMARK_WAIT_NS", "").strip()
    return int(v) if v else 1_000_000
