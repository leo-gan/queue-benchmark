# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 7180 | 1.00× | 9 |
| spsc-ring | bytes | 16339 | 2.28× | 9 |
| steal-deque | bytes | 20574 | 2.87× | 9 |
| deque-lock | bytes | 21117 | 2.94× | 9 |
| asyncio.Queue | bytes | 50391 | 7.02× | 9 |
| queue.Queue | bytes | 61585 | 8.58× | 9 |
| janus | bytes | 113668 | 15.83× | 9 |
