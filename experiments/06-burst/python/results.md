# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 53331 | 1.00× | 9 |
| deque-lock | bytes | 182945 | 3.43× | 9 |
| steal-deque | bytes | 185690 | 3.48× | 9 |
| asyncio.Queue | bytes | 457684 | 8.58× | 9 |
| queue.Queue | bytes | 592798 | 11.12× | 9 |
| janus | bytes | 1066597 | 20.00× | 9 |
