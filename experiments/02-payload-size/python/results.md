# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 6774 | 1.00× | 9 |
| spsc-ring | bytes | 16490 | 2.43× | 9 |
| deque-lock | bytes | 18581 | 2.74× | 9 |
| steal-deque | bytes | 19244 | 2.84× | 9 |
| asyncio.Queue | bytes | 48591 | 7.17× | 9 |
| queue.Queue | bytes | 57422 | 8.48× | 9 |
| janus | bytes | 107732 | 15.90× | 9 |
