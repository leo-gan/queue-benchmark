# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 7856 | 1.00× | 9 |
| steal-deque | bytes | 10121 | 1.29× | 9 |
| mutex-queue | bytes | 11219 | 1.43× | 9 |
