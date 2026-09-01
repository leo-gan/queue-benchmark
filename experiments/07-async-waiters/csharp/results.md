# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | 1p32c | 30800 | 1.00× | 9 |
| ConcurrentQueue | 1p32c | 33400 | 1.08× | 9 |
| Channel | 1p32c | 71400 | 2.32× | 9 |
