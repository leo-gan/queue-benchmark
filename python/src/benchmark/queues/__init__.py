from .asyncio_queue import AsyncioQueue
from .locked_deque import DequeLockQueue
from .stdlib_queue import StdlibQueue

ALL_QUEUES = [DequeLockQueue(), StdlibQueue(), AsyncioQueue()]
