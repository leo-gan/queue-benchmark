# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 4685883 | 1.00× | 9 |
| deque-lock | bytes | 6423993 | 1.37× | 9 |
| queue.Queue | bytes | 7922307 | 1.69× | 9 |
| asyncio.Queue | bytes | 15422610 | 3.29× | 9 |
