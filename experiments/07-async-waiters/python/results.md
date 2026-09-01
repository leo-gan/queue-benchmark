# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p32c | 146681 | 1.00× | 9 |
| deque-lock | 1p32c | 1351719 | 9.22× | 9 |
| steal-deque | 1p32c | 1400350 | 9.55× | 9 |
| queue.Queue | 1p32c | 1413579 | 9.64× | 9 |
