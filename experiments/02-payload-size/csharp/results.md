# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 2700 | 1.00× | 9 |
| Queue+lock | bytes | 5600 | 2.07× | 9 |
| Channel | bytes | 13900 | 5.15× | 9 |
