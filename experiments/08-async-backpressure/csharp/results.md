# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 5000 | 1.00× | 9 |
| Queue+lock | bytes | 6000 | 1.20× | 9 |
| steal-deque | bytes | 10300 | 2.06× | 9 |
| Channel | bytes | 13400 | 2.68× | 9 |
