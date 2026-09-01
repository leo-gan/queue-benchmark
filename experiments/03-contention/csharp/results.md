# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 4p1c | 10000 | 1.00× | 9 |
| ConcurrentQueue | 4p4c | 13700 | 1.37× | 9 |
| Channel | 4p1c | 18800 | 1.88× | 9 |
| steal-deque | 1p4c | 23500 | 2.35× | 9 |
| steal-deque | 4p1c | 24000 | 2.40× | 9 |
| steal-deque | 4p4c | 27100 | 2.71× | 9 |
| Channel | 4p4c | 27200 | 2.72× | 9 |
| ConcurrentQueue | 1p4c | 64500 | 6.45× | 9 |
| Channel | 1p4c | 80600 | 8.06× | 9 |
