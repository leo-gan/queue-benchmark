# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 6235451 | 1.00× | 9 |
| deque-lock | bytes | 6479441 | 1.04× | 9 |
| queue.Queue | bytes | 8032424 | 1.29× | 9 |
| janus | bytes | 17678388 | 2.84× | 9 |
| asyncio.Queue | bytes | 21675196 | 3.48× | 9 |
