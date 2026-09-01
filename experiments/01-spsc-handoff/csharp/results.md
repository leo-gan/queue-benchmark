# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 3000 | 1.00× | 9 |
| Queue+lock | bytes | 6400 | 2.13× | 9 |
| steal-deque | bytes | 9700 | 3.23× | 9 |
| Channel | bytes | 14200 | 4.73× | 9 |
