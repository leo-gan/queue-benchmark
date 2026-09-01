# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| Queue+lock | bytes | 107609500 | 1.00× | 9 |
| ConcurrentQueue | bytes | 110919400 | 1.03× | 9 |
| Channel | bytes | 113378000 | 1.05× | 9 |
