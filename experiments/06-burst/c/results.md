# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 11075 | 1.00× | 9 |
| mutex-queue | bytes | 32669 | 2.95× | 9 |
| steal-deque | bytes | 34061 | 3.08× | 9 |
