# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 735 | 1.00× | 9 |
| steal-deque | bytes | 2172 | 2.96× | 9 |
| mutex-queue | bytes | 2177 | 2.96× | 9 |
