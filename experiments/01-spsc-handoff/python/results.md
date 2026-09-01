# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 6973 | 1.00× | 9 |
| spsc-ring | bytes | 16104 | 2.31× | 9 |
| steal-deque | bytes | 20207 | 2.90× | 9 |
| deque-lock | bytes | 20327 | 2.92× | 9 |
| asyncio.Queue | bytes | 49023 | 7.03× | 9 |
| queue.Queue | bytes | 60495 | 8.68× | 9 |
| janus | bytes | 111546 | 16.00× | 9 |
