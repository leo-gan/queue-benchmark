# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 751 | 1.00× | 9 |
| steal-deque | bytes | 2236 | 2.98× | 9 |
| mutex-queue | bytes | 2237 | 2.98× | 9 |
