# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 5300 | 1.00× | 9 |
| Queue+lock | bytes | 6400 | 1.21× | 9 |
| steal-deque | bytes | 10100 | 1.91× | 9 |
| Channel | bytes | 14600 | 2.75× | 9 |
