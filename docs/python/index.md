# Python

| | |
|--|--|
| Runner | `python/` |
| Script | `./python/scripts/run-benchmarks.sh smoke` |
| Logs | `logs/python/` |
| Runtime | CPython 3.12+ via [uv](https://docs.astral.sh/uv/) |

| Log name | Category | Communication | Package | Notes |
|----------|----------|---------------|---------|-------|
| `deque-lock` | locked | T (thread) | stdlib | `collections.deque` + `threading.Lock` |
| `queue.Queue` | concurrent | T (thread) | stdlib | Threading MPMC blocking queue |
| `asyncio.Queue` | async | A (async) | stdlib | Event-loop queue |
| `spsc-ring` | spsc | T (thread) | harness | Single-producer ring; MPMC skipped |
| `steal-deque` | work-stealing | T (thread) | harness | Owner-push / steal-from-top |
| `multiprocessing.Queue` | concurrent | P (process) | stdlib | Opt-in two-process IPC |
| `shared-ring` | spsc | S (shared) | harness | Opt-in two-process mapped ring |
| `sqlite-queue` | durable | D (durable) | stdlib | Opt-in SQLite queue |

SPSC is one producer / one consumer. MPMC is two producers / two consumers
(CSV still logs `bytes` / `stream`). Compare T libraries separately from A.
See [Benchmark design](../analysis/BENCHMARK_DESIGN.md).
