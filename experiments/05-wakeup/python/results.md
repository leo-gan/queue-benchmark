# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.Queue | bytes | 109412118 | 1.00× | 9 |
| queue.SimpleQueue | bytes | 110519094 | 1.01× | 9 |
| asyncio.Queue | bytes | 129739608 | 1.19× | 9 |
| janus | bytes | 132411326 | 1.21× | 9 |
| deque-lock | bytes | 885037370 | 8.09× | 9 |
| steal-deque | bytes | 890891638 | 8.14× | 9 |
