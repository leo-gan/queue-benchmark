# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.Queue | bytes | 112325395 | 1.00× | 9 |
| asyncio.Queue | bytes | 127273534 | 1.13× | 9 |
| steal-deque | bytes | 900102571 | 8.01× | 9 |
| deque-lock | bytes | 915742601 | 8.15× | 9 |
