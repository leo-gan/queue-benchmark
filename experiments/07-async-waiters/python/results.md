# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p32c | 205662 | 1.00× | 9 |
| steal-deque | 1p32c | 1505681 | 7.32× | 9 |
| deque-lock | 1p32c | 2210303 | 10.75× | 9 |
| queue.Queue | 1p32c | 2340069 | 11.38× | 9 |
