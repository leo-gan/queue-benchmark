# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 173471 | 1.00× | 9 |
| steal-deque | bytes | 178134 | 1.03× | 9 |
| asyncio.Queue | bytes | 448830 | 2.59× | 9 |
| queue.Queue | bytes | 592048 | 3.41× | 9 |
