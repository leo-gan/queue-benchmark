# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 5200 | 1.00× | 9 |
| Queue+lock | bytes | 6900 | 1.33× | 9 |
| steal-deque | bytes | 10300 | 1.98× | 9 |
| Channel | bytes | 13600 | 2.62× | 9 |
