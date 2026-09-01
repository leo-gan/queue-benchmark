# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6110448 | 1.00× | 9 |
| steal-deque | bytes | 7554634 | 1.24× | 9 |
| queue.Queue | bytes | 7821183 | 1.28× | 9 |
| asyncio.Queue | bytes | 16586153 | 2.71× | 9 |
| janus | bytes | 17624786 | 2.88× | 9 |
