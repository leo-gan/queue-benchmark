# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 751 | 1.00× | 9 |
| steal-deque | bytes | 2235 | 2.98× | 9 |
| mutex-queue | bytes | 2240 | 2.98× | 9 |
| pipe-ipc | bytes | 129282 | 172.15× | 9 |
