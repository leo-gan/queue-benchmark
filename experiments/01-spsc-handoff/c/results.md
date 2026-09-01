# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 750 | 1.00× | 9 |
| steal-deque | bytes | 2238 | 2.98× | 9 |
| mutex-queue | bytes | 2239 | 2.99× | 9 |
