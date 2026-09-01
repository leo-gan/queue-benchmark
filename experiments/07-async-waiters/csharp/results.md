# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| Channel | 1p32c | 29200 | 1.00× | 9 |
| steal-deque | 1p32c | 35700 | 1.22× | 9 |
| ConcurrentQueue | 1p32c | 63000 | 2.16× | 9 |
