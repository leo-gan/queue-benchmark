# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| spsc-ring | bytes | 8819 | 1.00× | 9 |
| steal-deque | bytes | 10578 | 1.20× | 9 |
| mutex-queue | bytes | 21779 | 2.47× | 9 |
| lfqueue | bytes | 171711 | 19.47× | 9 |
