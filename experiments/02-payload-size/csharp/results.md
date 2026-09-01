# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 2900 | 1.00× | 9 |
| Queue+lock | bytes | 10200 | 3.52× | 9 |
| BlockingCollection | bytes | 10300 | 3.55× | 9 |
| steal-deque | bytes | 11200 | 3.86× | 9 |
| Channel | bytes | 15800 | 5.45× | 9 |
