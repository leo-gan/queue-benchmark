# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | 4p1c | 53639 | 1.00× | 9 |
| steal-deque | 4p4c | 83789 | 1.56× | 9 |
| mutex-queue | 4p4c | 87688 | 1.63× | 9 |
| lfqueue | 4p4c | 93274 | 1.74× | 9 |
| lfqueue | 4p1c | 97988 | 1.83× | 9 |
| mutex-queue | 4p1c | 99128 | 1.85× | 9 |
| steal-deque | 1p4c | 105264 | 1.96× | 9 |
| lfqueue | 1p4c | 131562 | 2.45× | 9 |
| mutex-queue | 1p4c | 154096 | 2.87× | 9 |
