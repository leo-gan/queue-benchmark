# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 4p1c | 96572 | 1.00× | 9 |
| asyncio.Queue | 4p4c | 109063 | 1.13× | 9 |
| asyncio.Queue | 1p4c | 117377 | 1.22× | 9 |
| janus | 4p1c | 168593 | 1.75× | 9 |
| janus | 1p4c | 181100 | 1.88× | 9 |
| janus | 4p4c | 192211 | 1.99× | 9 |
| queue.SimpleQueue | 1p4c | 208224 | 2.16× | 9 |
| queue.SimpleQueue | 4p1c | 209428 | 2.17× | 9 |
| deque-lock | 4p1c | 225431 | 2.33× | 9 |
| steal-deque | 1p4c | 233161 | 2.41× | 9 |
| deque-lock | 1p4c | 244091 | 2.53× | 9 |
| steal-deque | 4p1c | 256443 | 2.66× | 9 |
| queue.Queue | 1p4c | 287216 | 2.97× | 9 |
| queue.Queue | 4p1c | 299629 | 3.10× | 9 |
| queue.SimpleQueue | 4p4c | 334421 | 3.46× | 9 |
| steal-deque | 4p4c | 353669 | 3.66× | 9 |
| deque-lock | 4p4c | 380372 | 3.94× | 9 |
| queue.Queue | 4p4c | 420195 | 4.35× | 9 |
