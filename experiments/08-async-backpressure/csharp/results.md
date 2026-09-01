# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 2800 | 1.00× | 9 |
| Queue+lock | bytes | 6600 | 2.36× | 9 |
| steal-deque | bytes | 10200 | 3.64× | 9 |
| Channel | bytes | 14100 | 5.04× | 9 |
