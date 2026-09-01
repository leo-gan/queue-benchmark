# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p32c | 153379 | 1.00× | 9 |
| janus | 1p32c | 245344 | 1.60× | 9 |
| queue.SimpleQueue | 1p32c | 1659119 | 10.82× | 9 |
| deque-lock | 1p32c | 1676885 | 10.93× | 9 |
| steal-deque | 1p32c | 1715384 | 11.18× | 9 |
| queue.Queue | 1p32c | 1743658 | 11.37× | 9 |
