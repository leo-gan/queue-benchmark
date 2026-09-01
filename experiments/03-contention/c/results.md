# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| mutex-queue | 4p1c | 90346 | 1.00× | 9 |
| steal-deque | 4p1c | 94726 | 1.05× | 9 |
| mutex-queue | 1p4c | 95300 | 1.05× | 9 |
| steal-deque | 1p4c | 106632 | 1.18× | 9 |
| mutex-queue | 4p4c | 170172 | 1.88× | 9 |
| steal-deque | 4p4c | 179516 | 1.99× | 9 |
