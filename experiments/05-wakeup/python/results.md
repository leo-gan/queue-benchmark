# python

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | bytes | 116192677 | 1.00× | 9 |
| queue.Queue | bytes | 118307327 | 1.02× | 9 |
| asyncio.Queue | bytes | 131012701 | 1.13× | 9 |
| janus | bytes | 132331291 | 1.14× | 9 |
| deque-lock | bytes | 903366137 | 7.77× | 9 |
| steal-deque | bytes | 908629631 | 7.82× | 9 |
