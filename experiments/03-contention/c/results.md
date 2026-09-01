# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | 4p1c | 51078 | 1.00× | 9 |
| mutex-queue | 4p1c | 51353 | 1.01× | 9 |
| steal-deque | 1p4c | 52750 | 1.03× | 9 |
| mutex-queue | 1p4c | 86584 | 1.70× | 9 |
| mutex-queue | 4p4c | 87018 | 1.70× | 9 |
| steal-deque | 4p4c | 90279 | 1.77× | 9 |
