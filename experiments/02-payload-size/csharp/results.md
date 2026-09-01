# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 3000 | 1.00× | 9 |
| Queue+lock | bytes | 7200 | 2.40× | 9 |
| steal-deque | bytes | 10500 | 3.50× | 9 |
| Channel | bytes | 13700 | 4.57× | 9 |
