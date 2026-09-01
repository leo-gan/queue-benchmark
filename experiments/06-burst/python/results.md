# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 53195 | 1.00× | 9 |
| deque-lock | bytes | 172182 | 3.24× | 9 |
| steal-deque | bytes | 183051 | 3.44× | 9 |
| asyncio.Queue | bytes | 458214 | 8.61× | 9 |
| queue.Queue | bytes | 606687 | 11.40× | 9 |
| janus | bytes | 1066833 | 20.06× | 9 |
