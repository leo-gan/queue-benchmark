# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 1589 | 1.00× | 9 |
| steal-deque | bytes | 4732 | 2.98× | 9 |
| mutex-queue | bytes | 4742 | 2.98× | 9 |
