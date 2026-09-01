# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 872 | 1.00× | 9 |
| steal-deque | bytes | 2601 | 2.98× | 9 |
| mutex-queue | bytes | 2606 | 2.99× | 9 |
