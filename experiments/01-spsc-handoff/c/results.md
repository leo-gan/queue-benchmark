# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 901 | 1.00× | 9 |
| steal-deque | bytes | 2678 | 2.97× | 9 |
| mutex-queue | bytes | 2686 | 2.98× | 9 |
