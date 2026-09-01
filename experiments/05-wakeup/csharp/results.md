# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| BlockingCollection | bytes | 114007800 | 1.00× | 9 |
| Queue+lock | bytes | 114797100 | 1.01× | 9 |
| ConcurrentQueue | bytes | 115883300 | 1.02× | 9 |
| Channel | bytes | 117668900 | 1.03× | 9 |
