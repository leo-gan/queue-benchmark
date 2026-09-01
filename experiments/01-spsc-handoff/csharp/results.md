# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 3000 | 1.00× | 9 |
| Queue+lock | bytes | 6600 | 2.20× | 9 |
| steal-deque | bytes | 9500 | 3.17× | 9 |
| Channel | bytes | 13400 | 4.47× | 9 |
