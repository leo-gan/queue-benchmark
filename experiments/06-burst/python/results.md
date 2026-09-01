# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 54164 | 1.00× | 9 |
| steal-deque | bytes | 185161 | 3.42× | 9 |
| deque-lock | bytes | 192653 | 3.56× | 9 |
| asyncio.Queue | bytes | 465279 | 8.59× | 9 |
| queue.Queue | bytes | 614759 | 11.35× | 9 |
| janus | bytes | 1096845 | 20.25× | 9 |
