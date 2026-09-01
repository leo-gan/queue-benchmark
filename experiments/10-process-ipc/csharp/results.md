# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 3000 | 1.00× | 9 |
| Queue+lock | bytes | 6200 | 2.07× | 9 |
| steal-deque | bytes | 10400 | 3.47× | 9 |
| Channel | bytes | 14300 | 4.77× | 9 |
| pipe-ipc | bytes | 35011600 | 11670.53× | 9 |
