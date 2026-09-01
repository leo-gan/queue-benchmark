# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 16219 | 1.00× | 9 |
| deque-lock | bytes | 20185 | 1.24× | 9 |
| steal-deque | bytes | 20300 | 1.25× | 9 |
| asyncio.Queue | bytes | 46818 | 2.89× | 9 |
| queue.Queue | bytes | 58215 | 3.59× | 9 |
| multiprocessing.Queue | bytes | 42612828 | 2627.34× | 9 |
