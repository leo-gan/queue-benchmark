# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p4c | 101510 | 1.00× | 9 |
| asyncio.Queue | 4p4c | 113174 | 1.11× | 9 |
| asyncio.Queue | 4p1c | 130590 | 1.29× | 9 |
| deque-lock | 4p1c | 229710 | 2.26× | 9 |
| steal-deque | 1p4c | 242808 | 2.39× | 9 |
| deque-lock | 1p4c | 253674 | 2.50× | 9 |
| steal-deque | 4p1c | 316103 | 3.11× | 9 |
| queue.Queue | 1p4c | 316206 | 3.12× | 9 |
| queue.Queue | 4p1c | 318636 | 3.14× | 9 |
| deque-lock | 4p4c | 370438 | 3.65× | 9 |
| steal-deque | 4p4c | 371030 | 3.66× | 9 |
| queue.Queue | 4p4c | 461762 | 4.55× | 9 |
