# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 1p32c | 30500 | 1.00× | 9 |
| Channel | 1p32c | 38600 | 1.27× | 9 |
| steal-deque | 1p32c | 60700 | 1.99× | 9 |
