# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 15221 | 1.00× | 9 |
| steal-deque | bytes | 18780 | 1.23× | 9 |
| deque-lock | bytes | 19467 | 1.28× | 9 |
| asyncio.Queue | bytes | 44179 | 2.90× | 9 |
| queue.Queue | bytes | 56582 | 3.72× | 9 |
