# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p32c | 137935 | 1.00× | 9 |
| deque-lock | 1p32c | 1417081 | 10.27× | 9 |
| queue.Queue | 1p32c | 1421677 | 10.31× | 9 |
