# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 5200 | 1.00× | 9 |
| Queue+lock | bytes | 5900 | 1.13× | 9 |
| BlockingCollection | bytes | 8900 | 1.71× | 9 |
| steal-deque | bytes | 9900 | 1.90× | 9 |
| Channel | bytes | 14300 | 2.75× | 9 |
