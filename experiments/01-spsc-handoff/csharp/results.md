# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 5200 | 1.00× | 9 |
| Queue+lock | bytes | 5600 | 1.08× | 9 |
| steal-deque | bytes | 9700 | 1.87× | 9 |
| Channel | bytes | 13700 | 2.63× | 9 |
