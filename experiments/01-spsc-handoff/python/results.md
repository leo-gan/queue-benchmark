# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 7087 | 1.00× | 9 |
| spsc-ring | bytes | 16310 | 2.30× | 9 |
| deque-lock | bytes | 19967 | 2.82× | 9 |
| steal-deque | bytes | 20683 | 2.92× | 9 |
| asyncio.Queue | bytes | 48685 | 6.87× | 9 |
| queue.Queue | bytes | 59183 | 8.35× | 9 |
| janus | bytes | 112940 | 15.94× | 9 |
