# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 115572503 | 1.00× | 9 |
| queue.Queue | bytes | 120124148 | 1.04× | 9 |
| asyncio.Queue | bytes | 130097672 | 1.13× | 9 |
| janus | bytes | 136037146 | 1.18× | 9 |
| steal-deque | bytes | 910874365 | 7.88× | 9 |
| deque-lock | bytes | 939796517 | 8.13× | 9 |
