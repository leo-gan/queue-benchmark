# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6067553 | 1.00× | 9 |
| queue.Queue | bytes | 6327728 | 1.04× | 9 |
| steal-deque | bytes | 7238064 | 1.19× | 9 |
| janus | bytes | 18024582 | 2.97× | 9 |
| asyncio.Queue | bytes | 19283697 | 3.18× | 9 |
