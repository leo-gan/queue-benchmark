# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 14982 | 1.00× | 9 |
| deque-lock | bytes | 18874 | 1.26× | 9 |
| asyncio.Queue | bytes | 43606 | 2.91× | 9 |
| queue.Queue | bytes | 54817 | 3.66× | 9 |
