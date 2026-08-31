# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 3000 | 1.00× | 9 |
| Queue+lock | bytes | 6300 | 2.10× | 9 |
| Channel | bytes | 13500 | 4.50× | 9 |
