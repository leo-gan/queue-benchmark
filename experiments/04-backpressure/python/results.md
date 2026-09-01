# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6548909 | 1.00× | 9 |
| steal-deque | bytes | 7322991 | 1.12× | 9 |
| queue.Queue | bytes | 8240904 | 1.26× | 9 |
| asyncio.Queue | bytes | 16344784 | 2.50× | 9 |
| janus | bytes | 18992528 | 2.90× | 9 |
