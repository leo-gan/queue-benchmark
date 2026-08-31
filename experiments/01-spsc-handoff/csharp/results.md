# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 2800 | 1.00× | 9 |
| Queue+lock | bytes | 5800 | 2.07× | 9 |
| Channel | bytes | 14300 | 5.11× | 9 |
