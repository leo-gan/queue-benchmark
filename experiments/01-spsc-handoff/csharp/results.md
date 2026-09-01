# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 4500 | 1.00× | 9 |
| Queue+lock | bytes | 6200 | 1.38× | 9 |
| BlockingCollection | bytes | 9400 | 2.09× | 9 |
| steal-deque | bytes | 10200 | 2.27× | 9 |
| Channel | bytes | 14400 | 3.20× | 9 |
