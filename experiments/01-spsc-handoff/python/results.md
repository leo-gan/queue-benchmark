# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 16036 | 1.00× | 9 |
| deque-lock | bytes | 18334 | 1.14× | 9 |
| steal-deque | bytes | 18621 | 1.16× | 9 |
| asyncio.Queue | bytes | 45719 | 2.85× | 9 |
| queue.Queue | bytes | 58914 | 3.67× | 9 |
