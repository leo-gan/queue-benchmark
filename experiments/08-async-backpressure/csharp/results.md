# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 3000 | 1.00× | 9 |
| Queue+lock | bytes | 6200 | 2.07× | 9 |
| steal-deque | bytes | 10700 | 3.57× | 9 |
| Channel | bytes | 14400 | 4.80× | 9 |
