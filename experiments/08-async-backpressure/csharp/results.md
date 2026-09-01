# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 2800 | 1.00× | 9 |
| Queue+lock | bytes | 6600 | 2.36× | 9 |
| steal-deque | bytes | 10400 | 3.71× | 9 |
| Channel | bytes | 14400 | 5.14× | 9 |
