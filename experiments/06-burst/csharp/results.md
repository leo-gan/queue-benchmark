# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 36700 | 1.00× | 9 |
| Queue+lock | bytes | 60400 | 1.65× | 9 |
| steal-deque | bytes | 102100 | 2.78× | 9 |
| Channel | bytes | 124600 | 3.40× | 9 |
