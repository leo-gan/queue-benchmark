# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 39800 | 1.00× | 9 |
| Queue+lock | bytes | 68500 | 1.72× | 9 |
| steal-deque | bytes | 98500 | 2.47× | 9 |
| BlockingCollection | bytes | 106000 | 2.66× | 9 |
| Channel | bytes | 126400 | 3.18× | 9 |
