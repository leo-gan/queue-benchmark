# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 36500 | 1.00× | 9 |
| Queue+lock | bytes | 62700 | 1.72× | 9 |
| steal-deque | bytes | 94400 | 2.59× | 9 |
| BlockingCollection | bytes | 103300 | 2.83× | 9 |
| Channel | bytes | 126500 | 3.47× | 9 |
