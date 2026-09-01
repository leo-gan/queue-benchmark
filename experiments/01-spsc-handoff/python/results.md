# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 6801 | 1.00× | 9 |
| spsc-ring | bytes | 16055 | 2.36× | 9 |
| deque-lock | bytes | 19720 | 2.90× | 9 |
| steal-deque | bytes | 20389 | 3.00× | 9 |
| asyncio.Queue | bytes | 54267 | 7.98× | 9 |
| queue.Queue | bytes | 57183 | 8.41× | 9 |
| janus | bytes | 108317 | 15.93× | 9 |
