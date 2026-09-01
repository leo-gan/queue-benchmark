# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6447802 | 1.00× | 9 |
| steal-deque | bytes | 6771765 | 1.05× | 9 |
| queue.Queue | bytes | 7955314 | 1.23× | 9 |
| janus | bytes | 18222134 | 2.83× | 9 |
| asyncio.Queue | bytes | 19042693 | 2.95× | 9 |
