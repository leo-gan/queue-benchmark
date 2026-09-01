# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 6911 | 1.00× | 9 |
| spsc-ring | bytes | 16014 | 2.32× | 9 |
| steal-deque | bytes | 19382 | 2.80× | 9 |
| deque-lock | bytes | 20105 | 2.91× | 9 |
| asyncio.Queue | bytes | 48471 | 7.01× | 9 |
| queue.Queue | bytes | 60577 | 8.77× | 9 |
| janus | bytes | 109103 | 15.79× | 9 |
