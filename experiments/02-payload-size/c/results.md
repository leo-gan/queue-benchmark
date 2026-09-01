# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 784 | 1.00× | 9 |
| steal-deque | bytes | 1073 | 1.37× | 9 |
| mutex-queue | bytes | 1077 | 1.37× | 9 |
