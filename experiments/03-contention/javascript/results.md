# javascript

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| fastq | 4p4c | 1665 | 1.00× | 9 |
| fastq | 4p1c | 2352 | 1.41× | 9 |
| steal-deque | 4p1c | 6904 | 4.15× | 9 |
| steal-deque | 4p4c | 6918 | 4.15× | 9 |
| fastq | 1p4c | 9371 | 5.63× | 9 |
| steal-deque | 1p4c | 9446 | 5.67× | 9 |
