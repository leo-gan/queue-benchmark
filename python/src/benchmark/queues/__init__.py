from .asyncio_queue import AsyncioQueue
from .durable_sqlite import DurableSqliteQueue
from .locked_deque import DequeLockQueue
from .process_queue import ProcessQueue
from .shared_ring import SharedRingQueue
from .spsc_ring import SpscRingQueue
from .steal_deque import StealDequeQueue
from .stdlib_queue import StdlibQueue

ALL_QUEUES = [
    DequeLockQueue(),
    StdlibQueue(),
    AsyncioQueue(),
    SpscRingQueue(),
    StealDequeQueue(),
    ProcessQueue(),
    SharedRingQueue(),
    DurableSqliteQueue(),
]
