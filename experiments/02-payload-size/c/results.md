# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 752 | 1.00× | 9 |
| steal-deque | bytes | 2235 | 2.97× | 9 |
| mutex-queue | bytes | 2240 | 2.98× | 9 |
