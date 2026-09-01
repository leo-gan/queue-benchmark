# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 4p4c | 20200 | 1.00× | 9 |
| Channel | 4p1c | 25000 | 1.24× | 9 |
| steal-deque | 4p1c | 28700 | 1.42× | 9 |
| ConcurrentQueue | 1p4c | 32100 | 1.59× | 9 |
| Channel | 4p4c | 39800 | 1.97× | 9 |
| steal-deque | 1p4c | 43300 | 2.14× | 9 |
| Channel | 1p4c | 50000 | 2.48× | 9 |
| steal-deque | 4p4c | 50400 | 2.50× | 9 |
| ConcurrentQueue | 4p1c | 63300 | 3.13× | 9 |
