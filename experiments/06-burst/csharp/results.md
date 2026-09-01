# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 36600 | 1.00× | 9 |
| Queue+lock | bytes | 68600 | 1.87× | 9 |
| steal-deque | bytes | 97300 | 2.66× | 9 |
| Channel | bytes | 124700 | 3.41× | 9 |
