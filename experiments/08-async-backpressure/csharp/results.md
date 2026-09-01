# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 4300 | 1.00× | 9 |
| Queue+lock | bytes | 6200 | 1.44× | 9 |
| BlockingCollection | bytes | 9800 | 2.28× | 9 |
| steal-deque | bytes | 10600 | 2.47× | 9 |
| Channel | bytes | 13900 | 3.23× | 9 |
