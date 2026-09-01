# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | 1p4c | 49643 | 1.00× | 9 |
| mutex-queue | 1p4c | 52054 | 1.05× | 9 |
| steal-deque | 4p1c | 52963 | 1.07× | 9 |
| mutex-queue | 4p1c | 55237 | 1.11× | 9 |
| mutex-queue | 4p4c | 87831 | 1.77× | 9 |
| steal-deque | 4p4c | 88562 | 1.78× | 9 |
