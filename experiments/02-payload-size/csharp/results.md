# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 4900 | 1.00× | 9 |
| Queue+lock | bytes | 5700 | 1.16× | 9 |
| steal-deque | bytes | 10100 | 2.06× | 9 |
| Channel | bytes | 12800 | 2.61× | 9 |
