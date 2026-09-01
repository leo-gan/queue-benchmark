# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| deque-lock | bytes | 6552024 | 1.00× | 9 |
| steal-deque | bytes | 7585935 | 1.16× | 9 |
| queue.Queue | bytes | 8073750 | 1.23× | 9 |
| asyncio.Queue | bytes | 15682384 | 2.39× | 9 |
| janus | bytes | 18902570 | 2.88× | 9 |
