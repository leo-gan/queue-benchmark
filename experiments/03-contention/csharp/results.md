# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 4p1c | 16500 | 1.00× | 9 |
| Channel | 4p1c | 19500 | 1.18× | 9 |
| steal-deque | 1p4c | 26200 | 1.59× | 9 |
| steal-deque | 4p1c | 27000 | 1.64× | 9 |
| steal-deque | 4p4c | 27400 | 1.66× | 9 |
| Channel | 1p4c | 27800 | 1.68× | 9 |
| ConcurrentQueue | 4p4c | 27800 | 1.68× | 9 |
| Channel | 4p4c | 28800 | 1.75× | 9 |
| ConcurrentQueue | 1p4c | 29500 | 1.79× | 9 |
