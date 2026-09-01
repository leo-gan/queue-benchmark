# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 2800 | 1.00× | 9 |
| Queue+lock | bytes | 6400 | 2.29× | 9 |
| steal-deque | bytes | 9700 | 3.46× | 9 |
| Channel | bytes | 14700 | 5.25× | 9 |
| pipe-ipc | bytes | 38528400 | 13760.14× | 9 |
