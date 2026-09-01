# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 3100 | 1.00× | 9 |
| Queue+lock | bytes | 6300 | 2.03× | 9 |
| BlockingCollection | bytes | 9500 | 3.06× | 9 |
| steal-deque | bytes | 10300 | 3.32× | 9 |
| Channel | bytes | 14600 | 4.71× | 9 |
| pipe-ipc | bytes | 39976600 | 12895.68× | 9 |
