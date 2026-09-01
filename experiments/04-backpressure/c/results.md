# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 758 | 1.00× | 9 |
| steal-deque | bytes | 1230 | 1.62× | 9 |
| mutex-queue | bytes | 2239 | 2.95× | 9 |
