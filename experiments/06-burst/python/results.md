# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 178290 | 1.00× | 9 |
| steal-deque | bytes | 188973 | 1.06× | 9 |
| asyncio.Queue | bytes | 475465 | 2.67× | 9 |
| queue.Queue | bytes | 601921 | 3.38× | 9 |
