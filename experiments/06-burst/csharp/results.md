# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 40300 | 1.00× | 9 |
| Queue+lock | bytes | 66800 | 1.66× | 9 |
| steal-deque | bytes | 110300 | 2.74× | 9 |
| Channel | bytes | 127100 | 3.15× | 9 |
