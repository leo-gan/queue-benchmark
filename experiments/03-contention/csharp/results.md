# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 4p1c | 9100 | 1.00× | 9 |
| ConcurrentQueue | 4p4c | 14900 | 1.64× | 9 |
| Channel | 4p1c | 16700 | 1.84× | 9 |
| steal-deque | 4p1c | 20800 | 2.29× | 9 |
| steal-deque | 4p4c | 26800 | 2.95× | 9 |
| Channel | 4p4c | 28000 | 3.08× | 9 |
| steal-deque | 1p4c | 29300 | 3.22× | 9 |
| Channel | 1p4c | 66600 | 7.32× | 9 |
| ConcurrentQueue | 1p4c | 86900 | 9.55× | 9 |
