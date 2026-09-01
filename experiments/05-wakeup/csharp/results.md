# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| Queue+lock | bytes | 110684800 | 1.00× | 9 |
| Channel | bytes | 110898400 | 1.00× | 9 |
| ConcurrentQueue | bytes | 112051700 | 1.01× | 9 |
