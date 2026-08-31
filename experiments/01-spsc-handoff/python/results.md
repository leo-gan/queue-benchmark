# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 16892 | 1.00× | 9 |
| deque-lock | bytes | 21121 | 1.25× | 9 |
| asyncio.Queue | bytes | 54015 | 3.20× | 9 |
| queue.Queue | bytes | 68638 | 4.06× | 9 |
