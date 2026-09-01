# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 6196450 | 1.00× | 9 |
| deque-lock | bytes | 6493656 | 1.05× | 9 |
| queue.Queue | bytes | 7167642 | 1.16× | 9 |
| asyncio.Queue | bytes | 30004329 | 4.84× | 9 |
