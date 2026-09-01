# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| mutex-queue | 1p4c | 81707 | 1.00× | 9 |
| steal-deque | 4p1c | 83987 | 1.03× | 9 |
| mutex-queue | 4p1c | 86447 | 1.06× | 9 |
| steal-deque | 1p4c | 86587 | 1.06× | 9 |
| mutex-queue | 4p4c | 167188 | 2.05× | 9 |
| steal-deque | 4p4c | 184518 | 2.26× | 9 |
