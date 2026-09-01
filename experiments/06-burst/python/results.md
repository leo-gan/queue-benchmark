# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 55711 | 1.00× | 9 |
| deque-lock | bytes | 185267 | 3.33× | 9 |
| steal-deque | bytes | 187687 | 3.37× | 9 |
| asyncio.Queue | bytes | 471493 | 8.46× | 9 |
| queue.Queue | bytes | 612987 | 11.00× | 9 |
| janus | bytes | 1137767 | 20.42× | 9 |
