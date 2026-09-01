# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p4c | 99610 | 1.00× | 9 |
| asyncio.Queue | 4p4c | 108746 | 1.09× | 9 |
| asyncio.Queue | 4p1c | 109830 | 1.10× | 9 |
| janus | 1p4c | 170541 | 1.71× | 9 |
| janus | 4p1c | 170626 | 1.71× | 9 |
| janus | 4p4c | 180341 | 1.81× | 9 |
| queue.SimpleQueue | 1p4c | 200747 | 2.02× | 9 |
| queue.SimpleQueue | 4p1c | 213479 | 2.14× | 9 |
| steal-deque | 4p1c | 227767 | 2.29× | 9 |
| deque-lock | 4p1c | 237472 | 2.38× | 9 |
| steal-deque | 1p4c | 253218 | 2.54× | 9 |
| deque-lock | 1p4c | 272773 | 2.74× | 9 |
| queue.Queue | 4p1c | 291575 | 2.93× | 9 |
| queue.Queue | 1p4c | 293081 | 2.94× | 9 |
| deque-lock | 4p4c | 358428 | 3.60× | 9 |
| steal-deque | 4p4c | 366915 | 3.68× | 9 |
| queue.SimpleQueue | 4p4c | 374912 | 3.76× | 9 |
| queue.Queue | 4p4c | 415620 | 4.17× | 9 |
