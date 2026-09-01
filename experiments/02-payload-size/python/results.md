# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 7500 | 1.00× | 9 |
| spsc-ring | bytes | 15919 | 2.12× | 9 |
| steal-deque | bytes | 19419 | 2.59× | 9 |
| deque-lock | bytes | 19516 | 2.60× | 9 |
| asyncio.Queue | bytes | 57016 | 7.60× | 9 |
| queue.Queue | bytes | 63367 | 8.45× | 9 |
| janus | bytes | 111266 | 14.84× | 9 |
