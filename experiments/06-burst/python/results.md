# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 52554 | 1.00× | 9 |
| deque-lock | bytes | 183185 | 3.49× | 9 |
| steal-deque | bytes | 185854 | 3.54× | 9 |
| asyncio.Queue | bytes | 448761 | 8.54× | 9 |
| queue.Queue | bytes | 589785 | 11.22× | 9 |
| janus | bytes | 1086545 | 20.67× | 9 |
