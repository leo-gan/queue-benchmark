# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 4000 | 1.00× | 9 |
| Queue+lock | bytes | 5600 | 1.40× | 9 |
| Channel | bytes | 11400 | 2.85× | 9 |
