# c

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | 4p1c | 113112 | 1.00× | 9 |
| lfqueue | 1p4c | 115893 | 1.02× | 9 |
| mutex-queue | 1p4c | 119209 | 1.05× | 9 |
| lfqueue | 4p1c | 138349 | 1.22× | 9 |
| steal-deque | 1p4c | 141639 | 1.25× | 9 |
| mutex-queue | 4p1c | 141723 | 1.25× | 9 |
| steal-deque | 4p4c | 146742 | 1.30× | 9 |
| lfqueue | 4p4c | 151704 | 1.34× | 9 |
| mutex-queue | 4p4c | 169664 | 1.50× | 9 |
