# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 41700 | 1.00× | 9 |
| Queue+lock | bytes | 68500 | 1.64× | 9 |
| steal-deque | bytes | 101200 | 2.43× | 9 |
| Channel | bytes | 131800 | 3.16× | 9 |
