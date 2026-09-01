# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 2900 | 1.00× | 9 |
| Queue+lock | bytes | 5800 | 2.00× | 9 |
| BlockingCollection | bytes | 9100 | 3.14× | 9 |
| steal-deque | bytes | 10800 | 3.72× | 9 |
| Channel | bytes | 14600 | 5.03× | 9 |
