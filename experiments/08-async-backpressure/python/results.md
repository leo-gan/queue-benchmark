# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6282298 | 1.00× | 9 |
| steal-deque | bytes | 6837696 | 1.09× | 9 |
| queue.Queue | bytes | 8621723 | 1.37× | 9 |
| asyncio.Queue | bytes | 17044899 | 2.71× | 9 |
