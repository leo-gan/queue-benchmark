# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6746758 | 1.00× | 9 |
| steal-deque | bytes | 7196332 | 1.07× | 9 |
| queue.Queue | bytes | 8167650 | 1.21× | 9 |
| asyncio.Queue | bytes | 16975153 | 2.52× | 9 |
