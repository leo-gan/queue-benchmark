# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.Queue | bytes | 115962148 | 1.00× | 9 |
| asyncio.Queue | bytes | 128961210 | 1.11× | 9 |
| steal-deque | bytes | 917316089 | 7.91× | 9 |
| deque-lock | bytes | 944977838 | 8.15× | 9 |
