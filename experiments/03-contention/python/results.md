# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p4c | 96271 | 1.00× | 9 |
| asyncio.Queue | 4p4c | 104223 | 1.08× | 9 |
| asyncio.Queue | 4p1c | 105011 | 1.09× | 9 |
| steal-deque | 1p4c | 224839 | 2.34× | 9 |
| deque-lock | 1p4c | 235124 | 2.44× | 9 |
| deque-lock | 4p1c | 236152 | 2.45× | 9 |
| steal-deque | 4p1c | 246468 | 2.56× | 9 |
| queue.Queue | 1p4c | 293926 | 3.05× | 9 |
| queue.Queue | 4p1c | 307044 | 3.19× | 9 |
| steal-deque | 4p4c | 354218 | 3.68× | 9 |
| deque-lock | 4p4c | 406576 | 4.22× | 9 |
| queue.Queue | 4p4c | 458795 | 4.77× | 9 |
