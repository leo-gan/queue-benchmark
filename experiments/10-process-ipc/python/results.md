# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 7141 | 1.00× | 9 |
| spsc-ring | bytes | 15425 | 2.16× | 9 |
| steal-deque | bytes | 19151 | 2.68× | 9 |
| deque-lock | bytes | 19351 | 2.71× | 9 |
| asyncio.Queue | bytes | 48919 | 6.85× | 9 |
| queue.Queue | bytes | 57893 | 8.11× | 9 |
| janus | bytes | 114080 | 15.98× | 9 |
| multiprocessing.SimpleQueue | bytes | 44095957 | 6175.04× | 9 |
| multiprocessing.Queue | bytes | 44382712 | 6215.20× | 9 |
