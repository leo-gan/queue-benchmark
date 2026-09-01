# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.Queue | bytes | 116657103 | 1.00× | 9 |
| queue.SimpleQueue | bytes | 117052869 | 1.00× | 9 |
| asyncio.Queue | bytes | 131513193 | 1.13× | 9 |
| janus | bytes | 132295678 | 1.13× | 9 |
| steal-deque | bytes | 914011449 | 7.84× | 9 |
| deque-lock | bytes | 918666054 | 7.87× | 9 |
