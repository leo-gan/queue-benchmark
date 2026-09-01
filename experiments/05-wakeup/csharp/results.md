# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 109956400 | 1.00× | 9 |
| Channel | bytes | 112262600 | 1.02× | 9 |
| BlockingCollection | bytes | 116069100 | 1.06× | 9 |
| Queue+lock | bytes | 116554100 | 1.06× | 9 |
