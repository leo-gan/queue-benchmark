# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 7229 | 1.00× | 9 |
| spsc-ring | bytes | 16587 | 2.29× | 9 |
| deque-lock | bytes | 19700 | 2.73× | 9 |
| steal-deque | bytes | 20763 | 2.87× | 9 |
| asyncio.Queue | bytes | 47865 | 6.62× | 9 |
| queue.Queue | bytes | 58912 | 8.15× | 9 |
| janus | bytes | 111060 | 15.36× | 9 |
| multiprocessing.Queue | bytes | 45152722 | 6246.05× | 9 |
| multiprocessing.SimpleQueue | bytes | 45808726 | 6336.80× | 9 |
