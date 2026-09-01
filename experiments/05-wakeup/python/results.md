# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.Queue | bytes | 115748834 | 1.00× | 9 |
| asyncio.Queue | bytes | 128646789 | 1.11× | 9 |
| deque-lock | bytes | 913742907 | 7.89× | 9 |
| steal-deque | bytes | 919477657 | 7.94× | 9 |
