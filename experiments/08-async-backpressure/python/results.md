# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6615904 | 1.00× | 9 |
| steal-deque | bytes | 7250072 | 1.10× | 9 |
| queue.Queue | bytes | 8256307 | 1.25× | 9 |
| asyncio.Queue | bytes | 15265042 | 2.31× | 9 |
| janus | bytes | 17472604 | 2.64× | 9 |
