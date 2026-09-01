# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p32c | 150335 | 1.00× | 9 |
| janus | 1p32c | 243246 | 1.62× | 9 |
| queue.SimpleQueue | 1p32c | 1346006 | 8.95× | 9 |
| deque-lock | 1p32c | 1375341 | 9.15× | 9 |
| queue.Queue | 1p32c | 1396024 | 9.29× | 9 |
| steal-deque | 1p32c | 1451645 | 9.66× | 9 |
