# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 750 | 1.00× | 9 |
| mutex-queue | bytes | 2244 | 2.99× | 9 |
| steal-deque | bytes | 2245 | 2.99× | 9 |
