# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p4c | 95853 | 1.00× | 9 |
| asyncio.Queue | 4p1c | 104149 | 1.09× | 9 |
| asyncio.Queue | 4p4c | 108455 | 1.13× | 9 |
| janus | 4p1c | 170235 | 1.78× | 9 |
| janus | 1p4c | 180306 | 1.88× | 9 |
| janus | 4p4c | 182747 | 1.91× | 9 |
| queue.SimpleQueue | 1p4c | 200411 | 2.09× | 9 |
| queue.SimpleQueue | 4p1c | 204105 | 2.13× | 9 |
| deque-lock | 4p1c | 227346 | 2.37× | 9 |
| steal-deque | 4p1c | 227595 | 2.37× | 9 |
| deque-lock | 1p4c | 231523 | 2.42× | 9 |
| steal-deque | 1p4c | 252130 | 2.63× | 9 |
| queue.Queue | 1p4c | 294836 | 3.08× | 9 |
| queue.Queue | 4p1c | 312352 | 3.26× | 9 |
| queue.SimpleQueue | 4p4c | 330631 | 3.45× | 9 |
| deque-lock | 4p4c | 347016 | 3.62× | 9 |
| steal-deque | 4p4c | 370019 | 3.86× | 9 |
| queue.Queue | 4p4c | 446115 | 4.65× | 9 |
