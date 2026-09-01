# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 945 | 1.00× | 9 |
| steal-deque | bytes | 1275 | 1.35× | 9 |
| mutex-queue | bytes | 2742 | 2.90× | 9 |
| lfqueue | bytes | 13431 | 14.21× | 9 |
