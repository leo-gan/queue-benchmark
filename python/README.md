# Python Queue Benchmark

In-process queues: `deque-lock` (baseline), `queue.Queue` / `queue.SimpleQueue`
(threading MPMC), `asyncio.Queue` and `janus` (event loop).

```bash
cd python
./scripts/run-benchmarks.sh smoke
./scripts/run-benchmarks.sh all-single
./scripts/run-benchmarks.sh custom 20 "queue.Queue" "message"
```

Logs: `logs/python/YYYY-MM-DD-HHMMSS.csv`.

| Log name | Category | Package | SPSC | MPMC |
|----------|----------|---------|------|------|
| `deque-lock` | locked | stdlib | yes | yes (lock) |
| `queue.Queue` | concurrent | stdlib | yes | yes |
| `queue.SimpleQueue` | concurrent | stdlib | yes | yes (unbounded) |
| `asyncio.Queue` | async | stdlib | yes | yes (async tasks) |
| `janus` | async | janus | yes | yes (async face) |
