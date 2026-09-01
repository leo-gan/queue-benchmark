# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 2900 | 1.00× | 9 |
| Queue+lock | bytes | 5900 | 2.03× | 9 |
| steal-deque | bytes | 10200 | 3.52× | 9 |
| Channel | bytes | 13500 | 4.66× | 9 |
