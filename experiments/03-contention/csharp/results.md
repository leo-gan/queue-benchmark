# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 1p4c | 20300 | 1.00× | 9 |
| ConcurrentQueue | 4p1c | 22000 | 1.08× | 9 |
| ConcurrentQueue | 4p4c | 29000 | 1.43× | 9 |
| Channel | 1p4c | 33300 | 1.64× | 9 |
| Channel | 4p1c | 33400 | 1.65× | 9 |
| Channel | 4p4c | 39800 | 1.96× | 9 |
