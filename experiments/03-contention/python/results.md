# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p4c | 96195 | 1.00× | 9 |
| asyncio.Queue | 4p1c | 98859 | 1.03× | 9 |
| asyncio.Queue | 4p4c | 108934 | 1.13× | 9 |
| janus | 4p1c | 170699 | 1.77× | 9 |
| janus | 1p4c | 181054 | 1.88× | 9 |
| janus | 4p4c | 195578 | 2.03× | 9 |
| queue.SimpleQueue | 4p1c | 201710 | 2.10× | 9 |
| queue.SimpleQueue | 1p4c | 204057 | 2.12× | 9 |
| deque-lock | 4p1c | 228317 | 2.37× | 9 |
| deque-lock | 1p4c | 229059 | 2.38× | 9 |
| steal-deque | 1p4c | 229925 | 2.39× | 9 |
| steal-deque | 4p1c | 266992 | 2.78× | 9 |
| queue.Queue | 1p4c | 284238 | 2.95× | 9 |
| queue.Queue | 4p1c | 289082 | 3.01× | 9 |
| deque-lock | 4p4c | 371633 | 3.86× | 9 |
| steal-deque | 4p4c | 453680 | 4.72× | 9 |
| queue.SimpleQueue | 4p4c | 475934 | 4.95× | 9 |
| queue.Queue | 4p4c | 626996 | 6.52× | 9 |
