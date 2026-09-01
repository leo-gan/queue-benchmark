# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p32c | 144132 | 1.00× | 9 |
| janus | 1p32c | 217359 | 1.51× | 9 |
| queue.Queue | 1p32c | 1365070 | 9.47× | 9 |
| deque-lock | 1p32c | 1455124 | 10.10× | 9 |
| queue.SimpleQueue | 1p32c | 1483286 | 10.29× | 9 |
| steal-deque | 1p32c | 1502204 | 10.42× | 9 |
