# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 4955683 | 1.00× | 9 |
| deque-lock | bytes | 6456969 | 1.30× | 9 |
| queue.Queue | bytes | 7770904 | 1.57× | 9 |
| asyncio.Queue | bytes | 17639622 | 3.56× | 9 |
