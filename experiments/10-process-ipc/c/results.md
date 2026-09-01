# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 1083 | 1.00× | 9 |
| mutex-queue | bytes | 1460 | 1.35× | 9 |
| steal-deque | bytes | 1503 | 1.39× | 9 |
| lfqueue | bytes | 15398 | 14.22× | 9 |
| pipe-ipc | bytes | 180863 | 167.00× | 9 |
