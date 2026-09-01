# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 116035477 | 1.00× | 9 |
| queue.Queue | bytes | 116277195 | 1.00× | 9 |
| asyncio.Queue | bytes | 131425833 | 1.13× | 9 |
| janus | bytes | 134842944 | 1.16× | 9 |
| steal-deque | bytes | 911301933 | 7.85× | 9 |
| deque-lock | bytes | 917357603 | 7.91× | 9 |
