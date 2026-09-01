# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6759039 | 1.00× | 9 |
| steal-deque | bytes | 7421678 | 1.10× | 9 |
| queue.Queue | bytes | 8203054 | 1.21× | 9 |
| asyncio.Queue | bytes | 18248132 | 2.70× | 9 |
