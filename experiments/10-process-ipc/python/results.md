# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 15165 | 1.00× | 9 |
| deque-lock | bytes | 18555 | 1.22× | 9 |
| asyncio.Queue | bytes | 43292 | 2.85× | 9 |
| queue.Queue | bytes | 57947 | 3.82× | 9 |
| multiprocessing.Queue | bytes | 1333981 | 87.96× | 9 |
