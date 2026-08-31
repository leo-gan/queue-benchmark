# Python Queue Benchmark

In-process queues: `deque-lock` (baseline), `queue.Queue` (threading MPMC),
`asyncio.Queue` (event loop).

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
| `asyncio.Queue` | async | stdlib | yes | yes (async tasks) |
