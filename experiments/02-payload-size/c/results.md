# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 1126 | 1.00× | 9 |
| steal-deque | bytes | 3367 | 2.99× | 9 |
| mutex-queue | bytes | 3395 | 3.02× | 9 |
