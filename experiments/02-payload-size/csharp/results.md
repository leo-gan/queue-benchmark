# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 2700 | 1.00× | 9 |
| Queue+lock | bytes | 6300 | 2.33× | 9 |
| Channel | bytes | 11400 | 4.22× | 9 |
