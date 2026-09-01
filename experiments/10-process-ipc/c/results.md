# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 844 | 1.00× | 9 |
| steal-deque | bytes | 2514 | 2.98× | 9 |
| mutex-queue | bytes | 2516 | 2.98× | 9 |
| pipe-ipc | bytes | 128141 | 151.83× | 9 |
