# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 7589 | 1.00× | 9 |
| steal-deque | bytes | 22387 | 2.95× | 9 |
| mutex-queue | bytes | 22399 | 2.95× | 9 |
