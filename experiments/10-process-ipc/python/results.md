# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 7172 | 1.00× | 9 |
| spsc-ring | bytes | 15784 | 2.20× | 9 |
| steal-deque | bytes | 19568 | 2.73× | 9 |
| deque-lock | bytes | 20906 | 2.91× | 9 |
| asyncio.Queue | bytes | 48665 | 6.79× | 9 |
| queue.Queue | bytes | 61007 | 8.51× | 9 |
| janus | bytes | 109432 | 15.26× | 9 |
| multiprocessing.Queue | bytes | 43283881 | 6035.12× | 9 |
| multiprocessing.SimpleQueue | bytes | 44798184 | 6246.26× | 9 |
