# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 35000 | 1.00× | 9 |
| Queue+lock | bytes | 62300 | 1.78× | 9 |
| steal-deque | bytes | 88500 | 2.53× | 9 |
| Channel | bytes | 120500 | 3.44× | 9 |
