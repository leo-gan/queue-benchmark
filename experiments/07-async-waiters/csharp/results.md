# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 1p32c | 32900 | 1.00× | 9 |
| Channel | 1p32c | 33700 | 1.02× | 9 |
| steal-deque | 1p32c | 89800 | 2.73× | 9 |
