# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 772 | 1.00× | 9 |
| mutex-queue | bytes | 2298 | 2.98× | 9 |
| steal-deque | bytes | 2300 | 2.98× | 9 |
