# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p32c | 170565 | 1.00× | 9 |
| janus | 1p32c | 232809 | 1.36× | 9 |
| deque-lock | 1p32c | 1447443 | 8.49× | 9 |
| steal-deque | 1p32c | 1528431 | 8.96× | 9 |
| queue.Queue | 1p32c | 1660404 | 9.73× | 9 |
| queue.SimpleQueue | 1p32c | 1703054 | 9.98× | 9 |
