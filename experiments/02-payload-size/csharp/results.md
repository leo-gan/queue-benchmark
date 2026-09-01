# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 5600 | 1.00× | 9 |
| Queue+lock | bytes | 6300 | 1.12× | 9 |
| steal-deque | bytes | 10600 | 1.89× | 9 |
| Channel | bytes | 14100 | 2.52× | 9 |
