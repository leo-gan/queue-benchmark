# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 16579 | 1.00× | 9 |
| deque-lock | bytes | 19902 | 1.20× | 9 |
| steal-deque | bytes | 20698 | 1.25× | 9 |
| asyncio.Queue | bytes | 48951 | 2.95× | 9 |
| queue.Queue | bytes | 58445 | 3.53× | 9 |
| multiprocessing.Queue | bytes | 42861736 | 2585.30× | 9 |
