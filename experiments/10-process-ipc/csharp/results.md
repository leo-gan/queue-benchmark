# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 2800 | 1.00× | 9 |
| Queue+lock | bytes | 5900 | 2.11× | 9 |
| BlockingCollection | bytes | 9000 | 3.21× | 9 |
| steal-deque | bytes | 9900 | 3.54× | 9 |
| Channel | bytes | 14000 | 5.00× | 9 |
| pipe-ipc | bytes | 41893400 | 14961.93× | 9 |
