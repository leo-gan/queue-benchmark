# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 7431 | 1.00× | 9 |
| spsc-ring | bytes | 15776 | 2.12× | 9 |
| deque-lock | bytes | 19690 | 2.65× | 9 |
| steal-deque | bytes | 19727 | 2.65× | 9 |
| asyncio.Queue | bytes | 51893 | 6.98× | 9 |
| queue.Queue | bytes | 58301 | 7.85× | 9 |
| janus | bytes | 112837 | 15.18× | 9 |
