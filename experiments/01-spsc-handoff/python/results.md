# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 16534 | 1.00× | 9 |
| steal-deque | bytes | 18295 | 1.11× | 9 |
| deque-lock | bytes | 19378 | 1.17× | 9 |
| asyncio.Queue | bytes | 44716 | 2.70× | 9 |
| queue.Queue | bytes | 56944 | 3.44× | 9 |
