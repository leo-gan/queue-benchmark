# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 15471 | 1.00× | 9 |
| deque-lock | bytes | 17812 | 1.15× | 9 |
| steal-deque | bytes | 19101 | 1.23× | 9 |
| asyncio.Queue | bytes | 44223 | 2.86× | 9 |
| queue.Queue | bytes | 54513 | 3.52× | 9 |
