# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | bytes | 36500 | 1.00× | 9 |
| Queue+lock | bytes | 60800 | 1.67× | 9 |
| steal-deque | bytes | 94200 | 2.58× | 9 |
| BlockingCollection | bytes | 97300 | 2.67× | 9 |
| Channel | bytes | 128700 | 3.53× | 9 |
