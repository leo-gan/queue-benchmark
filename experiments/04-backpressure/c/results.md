# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 931 | 1.00× | 9 |
| steal-deque | bytes | 2797 | 3.00× | 9 |
| mutex-queue | bytes | 2805 | 3.01× | 9 |
