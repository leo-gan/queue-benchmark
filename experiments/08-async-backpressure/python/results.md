# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6677394 | 1.00× | 9 |
| steal-deque | bytes | 7364389 | 1.10× | 9 |
| queue.Queue | bytes | 8112188 | 1.21× | 9 |
| janus | bytes | 17178730 | 2.57× | 9 |
| asyncio.Queue | bytes | 17672085 | 2.65× | 9 |
