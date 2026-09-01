# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 1p32c | 27500 | 1.00× | 9 |
| BlockingCollection | 1p32c | 28100 | 1.02× | 9 |
| Channel | 1p32c | 34300 | 1.25× | 9 |
| steal-deque | 1p32c | 35600 | 1.29× | 9 |
