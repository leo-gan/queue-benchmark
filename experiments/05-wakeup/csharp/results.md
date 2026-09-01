# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 112884200 | 1.00× | 9 |
| Queue+lock | bytes | 113158000 | 1.00× | 9 |
| Channel | bytes | 116309800 | 1.03× | 9 |
