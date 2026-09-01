# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p32c | 144307 | 1.00× | 9 |
| steal-deque | 1p32c | 1332916 | 9.24× | 9 |
| queue.Queue | 1p32c | 1441615 | 9.99× | 9 |
| deque-lock | 1p32c | 1473006 | 10.21× | 9 |
