# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 6658 | 1.00× | 9 |
| spsc-ring | bytes | 15235 | 2.29× | 9 |
| steal-deque | bytes | 18892 | 2.84× | 9 |
| deque-lock | bytes | 21898 | 3.29× | 9 |
| asyncio.Queue | bytes | 47398 | 7.12× | 9 |
| queue.Queue | bytes | 55812 | 8.38× | 9 |
| janus | bytes | 108252 | 16.26× | 9 |
| multiprocessing.SimpleQueue | bytes | 45179294 | 6785.72× | 9 |
| multiprocessing.Queue | bytes | 45209747 | 6790.29× | 9 |
