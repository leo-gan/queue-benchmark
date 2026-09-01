# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 856 | 1.00× | 9 |
| mutex-queue | bytes | 1172 | 1.37× | 9 |
| steal-deque | bytes | 1173 | 1.37× | 9 |
