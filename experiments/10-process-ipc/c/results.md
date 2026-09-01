# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 1502 | 1.00× | 9 |
| steal-deque | bytes | 4471 | 2.98× | 9 |
| mutex-queue | bytes | 4510 | 3.00× | 9 |
| pipe-ipc | bytes | 224598 | 149.53× | 9 |
