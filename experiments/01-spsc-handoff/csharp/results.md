# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 2900 | 1.00× | 9 |
| Queue+lock | bytes | 6200 | 2.14× | 9 |
| BlockingCollection | bytes | 9800 | 3.38× | 9 |
| steal-deque | bytes | 10500 | 3.62× | 9 |
| Channel | bytes | 13000 | 4.48× | 9 |
