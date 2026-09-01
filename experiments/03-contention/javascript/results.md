# javascript

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| fastq | 4p4c | 1508 | 1.00× | 9 |
| fastq | 4p1c | 2419 | 1.60× | 9 |
| steal-deque | 4p1c | 7191 | 4.77× | 9 |
| steal-deque | 4p4c | 7254 | 4.81× | 9 |
| steal-deque | 1p4c | 9652 | 6.40× | 9 |
| fastq | 1p4c | 14633 | 9.70× | 9 |
