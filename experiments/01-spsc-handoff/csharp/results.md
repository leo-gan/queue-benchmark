# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 5300 | 1.00× | 9 |
| Queue+lock | bytes | 5800 | 1.09× | 9 |
| BlockingCollection | bytes | 9700 | 1.83× | 9 |
| steal-deque | bytes | 10300 | 1.94× | 9 |
| Channel | bytes | 14900 | 2.81× | 9 |
