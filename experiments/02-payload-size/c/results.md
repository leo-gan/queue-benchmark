# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 731 | 1.00× | 9 |
| steal-deque | bytes | 2173 | 2.97× | 9 |
| mutex-queue | bytes | 2176 | 2.98× | 9 |
