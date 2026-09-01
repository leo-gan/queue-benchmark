# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | 4p1c | 60556 | 1.00× | 9 |
| mutex-queue | 4p1c | 61643 | 1.02× | 9 |
| steal-deque | 1p4c | 66894 | 1.10× | 9 |
| mutex-queue | 1p4c | 93284 | 1.54× | 9 |
| steal-deque | 4p4c | 106089 | 1.75× | 9 |
| mutex-queue | 4p4c | 108430 | 1.79× | 9 |
