# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| Queue+lock | bytes | 112603100 | 1.00× | 9 |
| Channel | bytes | 113793700 | 1.01× | 9 |
| ConcurrentQueue | bytes | 114935600 | 1.02× | 9 |
