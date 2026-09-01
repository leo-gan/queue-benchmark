# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 2700 | 1.00× | 9 |
| Queue+lock | bytes | 5500 | 2.04× | 9 |
| steal-deque | bytes | 9500 | 3.52× | 9 |
| Channel | bytes | 13400 | 4.96× | 9 |
