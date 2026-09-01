# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 107744665 | 1.00× | 9 |
| queue.Queue | bytes | 117871202 | 1.09× | 9 |
| asyncio.Queue | bytes | 131333770 | 1.22× | 9 |
| janus | bytes | 138117351 | 1.28× | 9 |
| steal-deque | bytes | 902848650 | 8.38× | 9 |
| deque-lock | bytes | 905657735 | 8.41× | 9 |
