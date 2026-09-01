# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 4p1c | 10000 | 1.00× | 9 |
| ConcurrentQueue | 4p4c | 16200 | 1.62× | 9 |
| Channel | 4p1c | 20500 | 2.05× | 9 |
| steal-deque | 4p1c | 22100 | 2.21× | 9 |
| BlockingCollection | 4p4c | 22500 | 2.25× | 9 |
| BlockingCollection | 4p1c | 24400 | 2.44× | 9 |
| steal-deque | 4p4c | 25700 | 2.57× | 9 |
| steal-deque | 1p4c | 28500 | 2.85× | 9 |
| BlockingCollection | 1p4c | 33900 | 3.39× | 9 |
| ConcurrentQueue | 1p4c | 67600 | 6.76× | 9 |
| Channel | 1p4c | 82600 | 8.26× | 9 |
| Channel | 4p4c | 105900 | 10.59× | 9 |
