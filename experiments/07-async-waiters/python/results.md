# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| asyncio.Queue | 1p32c | 161909 | 1.00× | 9 |
| janus | 1p32c | 247021 | 1.53× | 9 |
| deque-lock | 1p32c | 1445553 | 8.93× | 9 |
| queue.SimpleQueue | 1p32c | 1455787 | 8.99× | 9 |
| steal-deque | 1p32c | 1461709 | 9.03× | 9 |
| queue.Queue | 1p32c | 1659843 | 10.25× | 9 |
