# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 4p1c | 104582 | 1.00× | 9 |
| asyncio.Queue | 1p4c | 112222 | 1.07× | 9 |
| asyncio.Queue | 4p4c | 117047 | 1.12× | 9 |
| janus | 4p1c | 180490 | 1.73× | 9 |
| janus | 4p4c | 203029 | 1.94× | 9 |
| janus | 1p4c | 203374 | 1.94× | 9 |
| queue.SimpleQueue | 4p1c | 213536 | 2.04× | 9 |
| deque-lock | 4p1c | 261771 | 2.50× | 9 |
| steal-deque | 4p1c | 267087 | 2.55× | 9 |
| steal-deque | 1p4c | 275255 | 2.63× | 9 |
| deque-lock | 1p4c | 275855 | 2.64× | 9 |
| queue.SimpleQueue | 1p4c | 279675 | 2.67× | 9 |
| queue.Queue | 1p4c | 295562 | 2.83× | 9 |
| queue.Queue | 4p1c | 325960 | 3.12× | 9 |
| queue.SimpleQueue | 4p4c | 352658 | 3.37× | 9 |
| steal-deque | 4p4c | 358334 | 3.43× | 9 |
| deque-lock | 4p4c | 395492 | 3.78× | 9 |
| queue.Queue | 4p4c | 411082 | 3.93× | 9 |
