# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 14910 | 1.00× | 9 |
| steal-deque | bytes | 18278 | 1.23× | 9 |
| deque-lock | bytes | 18737 | 1.26× | 9 |
| asyncio.Queue | bytes | 43603 | 2.92× | 9 |
| queue.Queue | bytes | 58697 | 3.94× | 9 |
| multiprocessing.Queue | bytes | 41481098 | 2782.10× | 9 |
