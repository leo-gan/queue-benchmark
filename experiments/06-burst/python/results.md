# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 54249 | 1.00× | 9 |
| deque-lock | bytes | 180571 | 3.33× | 9 |
| steal-deque | bytes | 185201 | 3.41× | 9 |
| asyncio.Queue | bytes | 477962 | 8.81× | 9 |
| queue.Queue | bytes | 601149 | 11.08× | 9 |
| janus | bytes | 1106693 | 20.40× | 9 |
