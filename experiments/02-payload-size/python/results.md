# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 7371 | 1.00× | 9 |
| spsc-ring | bytes | 16418 | 2.23× | 9 |
| steal-deque | bytes | 19809 | 2.69× | 9 |
| deque-lock | bytes | 20628 | 2.80× | 9 |
| asyncio.Queue | bytes | 50711 | 6.88× | 9 |
| queue.Queue | bytes | 62530 | 8.48× | 9 |
| janus | bytes | 115439 | 15.66× | 9 |
