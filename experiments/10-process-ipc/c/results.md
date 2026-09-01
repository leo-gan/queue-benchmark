# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 730 | 1.00× | 9 |
| mutex-queue | bytes | 2149 | 2.94× | 9 |
| steal-deque | bytes | 2167 | 2.97× | 9 |
| lfqueue | bytes | 15251 | 20.89× | 9 |
| pipe-ipc | bytes | 115939 | 158.82× | 9 |
