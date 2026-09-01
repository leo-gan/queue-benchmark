# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| BlockingCollection | 1p32c | 34900 | 1.00× | 9 |
| ConcurrentQueue | 1p32c | 70400 | 2.02× | 9 |
| steal-deque | 1p32c | 86400 | 2.48× | 9 |
| Channel | 1p32c | 113400 | 3.25× | 9 |
