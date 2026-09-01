# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 753 | 1.00× | 9 |
| steal-deque | bytes | 2232 | 2.96× | 9 |
| mutex-queue | bytes | 2313 | 3.07× | 9 |
| lfqueue | bytes | 15699 | 20.85× | 9 |
