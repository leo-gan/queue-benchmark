# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 4p1c | 9800 | 1.00× | 9 |
| ConcurrentQueue | 4p4c | 13200 | 1.35× | 9 |
| steal-deque | 4p1c | 17600 | 1.80× | 9 |
| Channel | 4p1c | 18100 | 1.85× | 9 |
| steal-deque | 4p4c | 23400 | 2.39× | 9 |
| BlockingCollection | 4p1c | 24300 | 2.48× | 9 |
| steal-deque | 1p4c | 27000 | 2.76× | 9 |
| ConcurrentQueue | 1p4c | 28100 | 2.87× | 9 |
| Channel | 4p4c | 28600 | 2.92× | 9 |
| BlockingCollection | 4p4c | 30700 | 3.13× | 9 |
| BlockingCollection | 1p4c | 33600 | 3.43× | 9 |
| Channel | 1p4c | 34400 | 3.51× | 9 |
