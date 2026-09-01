# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p4c | 97526 | 1.00× | 9 |
| asyncio.Queue | 4p1c | 98006 | 1.00× | 9 |
| asyncio.Queue | 4p4c | 110693 | 1.14× | 9 |
| steal-deque | 1p4c | 228190 | 2.34× | 9 |
| deque-lock | 4p1c | 234600 | 2.41× | 9 |
| steal-deque | 4p1c | 235450 | 2.41× | 9 |
| deque-lock | 1p4c | 260066 | 2.67× | 9 |
| queue.Queue | 4p1c | 304949 | 3.13× | 9 |
| queue.Queue | 1p4c | 310008 | 3.18× | 9 |
| steal-deque | 4p4c | 359653 | 3.69× | 9 |
| deque-lock | 4p4c | 387393 | 3.97× | 9 |
| queue.Queue | 4p4c | 424936 | 4.36× | 9 |
