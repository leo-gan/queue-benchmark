# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 752 | 1.00× | 9 |
| steal-deque | bytes | 2207 | 2.93× | 9 |
| mutex-queue | bytes | 2208 | 2.94× | 9 |
| lfqueue | bytes | 15665 | 20.83× | 9 |
