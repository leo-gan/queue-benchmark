# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 1085 | 1.00× | 9 |
| mutex-queue | bytes | 3183 | 2.93× | 9 |
| steal-deque | bytes | 3309 | 3.05× | 9 |
| lfqueue | bytes | 22559 | 20.79× | 9 |
