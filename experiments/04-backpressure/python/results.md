# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6142108 | 1.00× | 9 |
| steal-deque | bytes | 7475761 | 1.22× | 9 |
| queue.Queue | bytes | 7713169 | 1.26× | 9 |
| asyncio.Queue | bytes | 16547237 | 2.69× | 9 |
| janus | bytes | 18691503 | 3.04× | 9 |
