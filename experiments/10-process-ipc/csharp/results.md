# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 4800 | 1.00× | 9 |
| Queue+lock | bytes | 7300 | 1.52× | 9 |
| steal-deque | bytes | 10900 | 2.27× | 9 |
| BlockingCollection | bytes | 12100 | 2.52× | 9 |
| Channel | bytes | 22600 | 4.71× | 9 |
| pipe-ipc | bytes | 36653000 | 7636.04× | 9 |
