"""janus async face: asyncio-compatible MPMC, compared only in category A."""

from __future__ import annotations

from importlib.metadata import version
from typing import Any

import janus

from .base import QueueAdapter


class JanusQueue(QueueAdapter):
    name = "janus"
    category = "async"
    supports_mpmc = True
    is_async = True
    communication = "async"

    def version(self) -> str:
        return version("janus")

    def create(self, capacity: int | None = None) -> Any:
        return janus.Queue(maxsize=int(capacity) if capacity else 0)

    async def enqueue_async(self, q: Any, item: bytes) -> None:
        await q.async_q.put(item)

    async def dequeue_async(self, q: Any) -> bytes:
        return await q.async_q.get()

    async def close_async(self, q: Any) -> None:
        await q.aclose()
