# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 15685 | 1.00× | 9 |
| deque-lock | bytes | 19424 | 1.24× | 9 |
| steal-deque | bytes | 19635 | 1.25× | 9 |
| asyncio.Queue | bytes | 47507 | 3.03× | 9 |
| queue.Queue | bytes | 59113 | 3.77× | 9 |
