# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 784 | 1.00× | 9 |
| steal-deque | bytes | 1048 | 1.34× | 9 |
| mutex-queue | bytes | 1072 | 1.37× | 9 |
| lfqueue | bytes | 11305 | 14.42× | 9 |
