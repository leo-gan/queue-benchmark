# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| Queue+lock | bytes | 110474700 | 1.00× | 9 |
| ConcurrentQueue | bytes | 111715400 | 1.01× | 9 |
| Channel | bytes | 114843700 | 1.04× | 9 |
