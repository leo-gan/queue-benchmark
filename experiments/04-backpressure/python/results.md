# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6257911 | 1.00× | 9 |
| queue.Queue | bytes | 6328835 | 1.01× | 9 |
| steal-deque | bytes | 7485866 | 1.20× | 9 |
| janus | bytes | 17301124 | 2.76× | 9 |
| asyncio.Queue | bytes | 18434689 | 2.95× | 9 |
