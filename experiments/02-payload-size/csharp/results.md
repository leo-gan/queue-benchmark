# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 4700 | 1.00× | 9 |
| Queue+lock | bytes | 5600 | 1.19× | 9 |
| steal-deque | bytes | 9700 | 2.06× | 9 |
| BlockingCollection | bytes | 10600 | 2.26× | 9 |
| Channel | bytes | 13800 | 2.94× | 9 |
