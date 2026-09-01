# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 8400 | 1.00× | 9 |
| steal-deque | bytes | 10346 | 1.23× | 9 |
| mutex-queue | bytes | 10862 | 1.29× | 9 |
