# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 3900 | 1.00× | 9 |
| Queue+lock | bytes | 7300 | 1.87× | 9 |
| steal-deque | bytes | 11200 | 2.87× | 9 |
| Channel | bytes | 14000 | 3.59× | 9 |
| pipe-ipc | bytes | 43312800 | 11105.85× | 9 |
