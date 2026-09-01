# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 6786 | 1.00× | 9 |
| spsc-ring | bytes | 16159 | 2.38× | 9 |
| steal-deque | bytes | 19498 | 2.87× | 9 |
| deque-lock | bytes | 19958 | 2.94× | 9 |
| asyncio.Queue | bytes | 47232 | 6.96× | 9 |
| queue.Queue | bytes | 59583 | 8.78× | 9 |
| janus | bytes | 109243 | 16.10× | 9 |
| multiprocessing.SimpleQueue | bytes | 44735912 | 6592.38× | 9 |
| multiprocessing.Queue | bytes | 45371143 | 6685.99× | 9 |
