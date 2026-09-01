# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 178517 | 1.00× | 9 |
| steal-deque | bytes | 184861 | 1.04× | 9 |
| asyncio.Queue | bytes | 454539 | 2.55× | 9 |
| queue.Queue | bytes | 594466 | 3.33× | 9 |
