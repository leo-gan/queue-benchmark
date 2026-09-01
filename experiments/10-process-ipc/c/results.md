# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 752 | 1.00× | 9 |
| mutex-queue | bytes | 2240 | 2.98× | 9 |
| steal-deque | bytes | 2243 | 2.98× | 9 |
| pipe-ipc | bytes | 123797 | 164.62× | 9 |
