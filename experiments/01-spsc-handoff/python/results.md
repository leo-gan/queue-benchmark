# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 7182 | 1.00× | 9 |
| spsc-ring | bytes | 15782 | 2.20× | 9 |
| steal-deque | bytes | 19830 | 2.76× | 9 |
| deque-lock | bytes | 20303 | 2.83× | 9 |
| asyncio.Queue | bytes | 47217 | 6.57× | 9 |
| queue.Queue | bytes | 59204 | 8.24× | 9 |
| janus | bytes | 109455 | 15.24× | 9 |
