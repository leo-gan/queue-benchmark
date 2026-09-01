# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 799 | 1.00× | 9 |
| steal-deque | bytes | 2369 | 2.96× | 9 |
| mutex-queue | bytes | 2374 | 2.97× | 9 |
