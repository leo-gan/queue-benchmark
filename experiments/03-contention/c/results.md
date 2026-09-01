# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| mutex-queue | 4p1c | 58844 | 1.00× | 9 |
| mutex-queue | 1p4c | 61319 | 1.04× | 9 |
| steal-deque | 4p1c | 61427 | 1.04× | 9 |
| steal-deque | 1p4c | 61461 | 1.04× | 9 |
| steal-deque | 4p4c | 95815 | 1.63× | 9 |
| mutex-queue | 4p4c | 98827 | 1.68× | 9 |
