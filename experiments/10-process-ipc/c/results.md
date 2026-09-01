# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 819 | 1.00× | 9 |
| steal-deque | bytes | 2438 | 2.98× | 9 |
| mutex-queue | bytes | 2445 | 2.99× | 9 |
| pipe-ipc | bytes | 125689 | 153.47× | 9 |
