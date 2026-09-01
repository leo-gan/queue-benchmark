# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 783 | 1.00× | 9 |
| mutex-queue | bytes | 1078 | 1.38× | 9 |
| steal-deque | bytes | 1093 | 1.40× | 9 |
| pipe-ipc | bytes | 121858 | 155.63× | 9 |
