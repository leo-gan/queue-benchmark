# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p4c | 96997 | 1.00× | 9 |
| asyncio.Queue | 4p4c | 103790 | 1.07× | 9 |
| asyncio.Queue | 4p1c | 108625 | 1.12× | 9 |
| janus | 1p4c | 165471 | 1.71× | 9 |
| janus | 4p4c | 174757 | 1.80× | 9 |
| janus | 4p1c | 176988 | 1.82× | 9 |
| queue.SimpleQueue | 1p4c | 204771 | 2.11× | 9 |
| queue.SimpleQueue | 4p1c | 221464 | 2.28× | 9 |
| deque-lock | 4p1c | 230685 | 2.38× | 9 |
| steal-deque | 1p4c | 233503 | 2.41× | 9 |
| steal-deque | 4p1c | 235249 | 2.43× | 9 |
| deque-lock | 1p4c | 259173 | 2.67× | 9 |
| queue.Queue | 1p4c | 284069 | 2.93× | 9 |
| queue.Queue | 4p1c | 305555 | 3.15× | 9 |
| queue.SimpleQueue | 4p4c | 317868 | 3.28× | 9 |
| deque-lock | 4p4c | 351906 | 3.63× | 9 |
| steal-deque | 4p4c | 374146 | 3.86× | 9 |
| queue.Queue | 4p4c | 418776 | 4.32× | 9 |
