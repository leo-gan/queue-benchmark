# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 18672 | 1.00× | 9 |
| deque-lock | bytes | 19076 | 1.02× | 9 |
| steal-deque | bytes | 22498 | 1.20× | 9 |
| asyncio.Queue | bytes | 53809 | 2.88× | 9 |
| queue.Queue | bytes | 57087 | 3.06× | 9 |
