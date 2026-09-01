# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 818 | 1.00× | 9 |
| steal-deque | bytes | 1103 | 1.35× | 9 |
| mutex-queue | bytes | 1133 | 1.39× | 9 |
| lfqueue | bytes | 11847 | 14.48× | 9 |
