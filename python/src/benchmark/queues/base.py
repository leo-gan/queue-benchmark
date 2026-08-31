"""Queue adapter protocol."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class QueueAdapter(ABC):
    name: str
    category: str
    supports_mpmc: bool = True
    supports_spsc_only: bool = False
    is_async: bool = False
    communication: str = "thread"
    opt_in: bool = False

    @abstractmethod
    def version(self) -> str: ...

    @abstractmethod
    def create(self, capacity: int | None = None) -> Any: ...

    def enqueue(self, q: Any, item: bytes) -> None:
        raise NotImplementedError

    def dequeue(self, q: Any) -> bytes:
        raise NotImplementedError
