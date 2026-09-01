# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 1p32c | 32800 | 1.00× | 9 |
| Channel | 1p32c | 34500 | 1.05× | 9 |
| BlockingCollection | 1p32c | 39100 | 1.19× | 9 |
| steal-deque | 1p32c | 39500 | 1.20× | 9 |
