# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6390890 | 1.00× | 9 |
| queue.Queue | bytes | 7565835 | 1.18× | 9 |
| steal-deque | bytes | 7695682 | 1.20× | 9 |
| asyncio.Queue | bytes | 15745738 | 2.46× | 9 |
| janus | bytes | 17676738 | 2.77× | 9 |
