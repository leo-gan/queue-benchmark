# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 9172 | 1.00× | 9 |
| steal-deque | bytes | 27011 | 2.94× | 9 |
| mutex-queue | bytes | 37663 | 4.11× | 9 |
| lfqueue | bytes | 226805 | 24.73× | 9 |
