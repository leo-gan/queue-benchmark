# csharp

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 1p4c | 12100 | 1.00× | 9 |
| ConcurrentQueue | 4p1c | 13100 | 1.08× | 9 |
| ConcurrentQueue | 4p4c | 22000 | 1.82× | 9 |
| Channel | 1p4c | 22200 | 1.83× | 9 |
| Channel | 4p1c | 22300 | 1.84× | 9 |
| Channel | 4p4c | 30100 | 2.49× | 9 |
