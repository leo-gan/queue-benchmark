# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 750 | 1.00× | 9 |
| steal-deque | bytes | 2233 | 2.98× | 9 |
| mutex-queue | bytes | 2237 | 2.98× | 9 |
