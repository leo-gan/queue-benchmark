from __future__ import annotations

import asyncio
import platform
from typing import Any

from .base import QueueAdapter


class AsyncioQueue(QueueAdapter):
    name = "asyncio.Queue"
    category = "async"
    supports_mpmc = True
    is_async = True

    def version(self) -> str:
        return platform.python_version()

    def create(self, capacity: int | None = None) -> Any:
        return asyncio.Queue()

    async def enqueue_async(self, q: Any, item: bytes) -> None:
        await q.put(item)

    async def dequeue_async(self, q: Any) -> bytes:
        return await q.get()
