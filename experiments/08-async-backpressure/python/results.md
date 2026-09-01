# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 7023227 | 1.00× | 9 |
| steal-deque | bytes | 7654580 | 1.09× | 9 |
| queue.Queue | bytes | 8269262 | 1.18× | 9 |
| asyncio.Queue | bytes | 18313314 | 2.61× | 9 |
