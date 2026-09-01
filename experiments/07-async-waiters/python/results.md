# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p32c | 142329 | 1.00× | 9 |
| janus | 1p32c | 219617 | 1.54× | 9 |
| queue.SimpleQueue | 1p32c | 1307443 | 9.19× | 9 |
| deque-lock | 1p32c | 1407045 | 9.89× | 9 |
| steal-deque | 1p32c | 1411019 | 9.91× | 9 |
| queue.Queue | 1p32c | 1414945 | 9.94× | 9 |
