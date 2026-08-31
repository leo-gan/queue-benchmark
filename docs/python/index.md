# Python

| | |
|--|--|
| Runner | `python/` |
| Script | `./python/scripts/run-benchmarks.sh smoke` |
| Logs | `logs/python/` |
| Runtime | CPython 3.12+ via [uv](https://docs.astral.sh/uv/) |

| Log name | Category | Package | Notes |
|----------|----------|---------|-------|
| `deque-lock` | locked | stdlib | `collections.deque` + `threading.Lock` |
| `queue.Queue` | concurrent | stdlib | Threading MPMC blocking queue |
| `asyncio.Queue` | async | stdlib | Event-loop queue |

SPSC is sequential enqueue-then-dequeue. MPMC (`stream`) uses two producers and two consumers.
