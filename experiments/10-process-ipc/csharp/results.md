# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 4600 | 1.00× | 9 |
| Queue+lock | bytes | 5700 | 1.24× | 9 |
| steal-deque | bytes | 10500 | 2.28× | 9 |
| Channel | bytes | 14100 | 3.07× | 9 |
| pipe-ipc | bytes | 37959700 | 8252.11× | 9 |
