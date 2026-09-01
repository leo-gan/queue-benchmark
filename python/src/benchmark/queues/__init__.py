from .asyncio_queue import AsyncioQueue
from .durable_sqlite import DurableSqliteQueue
from .janus_queue import JanusQueue
from .locked_deque import DequeLockQueue
from .process_queue import ProcessQueue
from .process_simple_queue import ProcessSimpleQueue
from .shared_ring import SharedRingQueue
from .simple_queue import SimpleQueueAdapter
from .spsc_ring import SpscRingQueue
from .steal_deque import StealDequeQueue
from .stdlib_queue import StdlibQueue

ALL_QUEUES = [
    DequeLockQueue(),
    StdlibQueue(),
    SimpleQueueAdapter(),
    AsyncioQueue(),
    JanusQueue(),
    SpscRingQueue(),
    StealDequeQueue(),
    ProcessQueue(),
    ProcessSimpleQueue(),
    SharedRingQueue(),
    DurableSqliteQueue(),
]
