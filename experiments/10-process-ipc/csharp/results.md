# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 3600 | 1.00× | 9 |
| Queue+lock | bytes | 6900 | 1.92× | 9 |
| steal-deque | bytes | 10500 | 2.92× | 9 |
| Channel | bytes | 14600 | 4.06× | 9 |
| pipe-ipc | bytes | 36914900 | 10254.14× | 9 |
