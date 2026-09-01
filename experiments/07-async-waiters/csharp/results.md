# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | 1p32c | 41900 | 1.00× | 9 |
| ConcurrentQueue | 1p32c | 63600 | 1.52× | 9 |
| Channel | 1p32c | 85100 | 2.03× | 9 |
