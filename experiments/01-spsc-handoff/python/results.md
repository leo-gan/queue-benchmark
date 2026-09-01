# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 7068 | 1.00× | 9 |
| spsc-ring | bytes | 16070 | 2.27× | 9 |
| steal-deque | bytes | 19970 | 2.83× | 9 |
| deque-lock | bytes | 20667 | 2.92× | 9 |
| asyncio.Queue | bytes | 47362 | 6.70× | 9 |
| queue.Queue | bytes | 59443 | 8.41× | 9 |
| janus | bytes | 113956 | 16.12× | 9 |
