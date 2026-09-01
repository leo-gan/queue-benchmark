# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 7824 | 1.00× | 9 |
| spsc-ring | bytes | 16044 | 2.05× | 9 |
| steal-deque | bytes | 20146 | 2.57× | 9 |
| deque-lock | bytes | 20763 | 2.65× | 9 |
| asyncio.Queue | bytes | 49375 | 6.31× | 9 |
| queue.Queue | bytes | 66993 | 8.56× | 9 |
| janus | bytes | 112844 | 14.42× | 9 |
| multiprocessing.SimpleQueue | bytes | 44442846 | 5680.32× | 9 |
| multiprocessing.Queue | bytes | 44902731 | 5739.10× | 9 |
