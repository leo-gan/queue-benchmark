# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 4p1c | 98244 | 1.00× | 9 |
| asyncio.Queue | 1p4c | 102467 | 1.04× | 9 |
| asyncio.Queue | 4p4c | 115537 | 1.18× | 9 |
| deque-lock | 4p1c | 234531 | 2.39× | 9 |
| deque-lock | 1p4c | 245707 | 2.50× | 9 |
| queue.Queue | 4p1c | 287745 | 2.93× | 9 |
| queue.Queue | 1p4c | 292196 | 2.97× | 9 |
| deque-lock | 4p4c | 416681 | 4.24× | 9 |
| queue.Queue | 4p4c | 546829 | 5.57× | 9 |
