# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 7385 | 1.00× | 9 |
| steal-deque | bytes | 21759 | 2.95× | 9 |
| mutex-queue | bytes | 21771 | 2.95× | 9 |
