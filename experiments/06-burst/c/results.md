# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 9844 | 1.00× | 9 |
| mutex-queue | bytes | 27999 | 2.84× | 9 |
| steal-deque | bytes | 29017 | 2.95× | 9 |
