# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6200714 | 1.00× | 9 |
| steal-deque | bytes | 7199934 | 1.16× | 9 |
| queue.Queue | bytes | 8200396 | 1.32× | 9 |
| janus | bytes | 17738459 | 2.86× | 9 |
| asyncio.Queue | bytes | 19959521 | 3.22× | 9 |
