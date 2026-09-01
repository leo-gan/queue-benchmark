# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 3800 | 1.00× | 9 |
| Queue+lock | bytes | 5500 | 1.45× | 9 |
| Channel | bytes | 11100 | 2.92× | 9 |
