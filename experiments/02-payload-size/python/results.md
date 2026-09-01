# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 6977 | 1.00× | 9 |
| spsc-ring | bytes | 15991 | 2.29× | 9 |
| deque-lock | bytes | 19555 | 2.80× | 9 |
| steal-deque | bytes | 19613 | 2.81× | 9 |
| asyncio.Queue | bytes | 47866 | 6.86× | 9 |
| queue.Queue | bytes | 60989 | 8.74× | 9 |
| janus | bytes | 111516 | 15.98× | 9 |
