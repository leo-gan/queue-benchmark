# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6714420 | 1.00× | 9 |
| queue.Queue | bytes | 7239200 | 1.08× | 9 |
| steal-deque | bytes | 7323898 | 1.09× | 9 |
| asyncio.Queue | bytes | 16878832 | 2.51× | 9 |
