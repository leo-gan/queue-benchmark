# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 4p1c | 19900 | 1.00× | 9 |
| ConcurrentQueue | 4p4c | 20900 | 1.05× | 9 |
| Channel | 4p1c | 26700 | 1.34× | 9 |
| Channel | 1p4c | 30300 | 1.52× | 9 |
| steal-deque | 4p1c | 33100 | 1.66× | 9 |
| Channel | 4p4c | 34400 | 1.73× | 9 |
| steal-deque | 1p4c | 45000 | 2.26× | 9 |
| steal-deque | 4p4c | 49800 | 2.50× | 9 |
| ConcurrentQueue | 1p4c | 58600 | 2.94× | 9 |
