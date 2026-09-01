# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 3100 | 1.00× | 9 |
| Queue+lock | bytes | 8300 | 2.68× | 9 |
| steal-deque | bytes | 10700 | 3.45× | 9 |
| Channel | bytes | 14400 | 4.65× | 9 |
