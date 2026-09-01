# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 4p1c | 10600 | 1.00× | 9 |
| Channel | 4p1c | 26600 | 2.51× | 9 |
| Channel | 4p4c | 32100 | 3.03× | 9 |
| steal-deque | 1p4c | 33800 | 3.19× | 9 |
| steal-deque | 4p1c | 35200 | 3.32× | 9 |
| Channel | 1p4c | 38000 | 3.58× | 9 |
| BlockingCollection | 1p4c | 39100 | 3.69× | 9 |
| BlockingCollection | 4p1c | 44900 | 4.24× | 9 |
| ConcurrentQueue | 4p4c | 45800 | 4.32× | 9 |
| steal-deque | 4p4c | 46800 | 4.42× | 9 |
| BlockingCollection | 4p4c | 56700 | 5.35× | 9 |
| ConcurrentQueue | 1p4c | 71200 | 6.72× | 9 |
