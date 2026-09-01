# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| Queue+lock | bytes | 111891400 | 1.00× | 9 |
| ConcurrentQueue | bytes | 112942100 | 1.01× | 9 |
| BlockingCollection | bytes | 113982800 | 1.02× | 9 |
| Channel | bytes | 115138100 | 1.03× | 9 |
