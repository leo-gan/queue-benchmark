# javascript

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| fastq | 4p4c | 1483 | 1.00× | 9 |
| fastq | 4p1c | 2239 | 1.51× | 9 |
| steal-deque | 4p1c | 6939 | 4.68× | 9 |
| steal-deque | 4p4c | 7351 | 4.96× | 9 |
| steal-deque | 1p4c | 8897 | 6.00× | 9 |
| fastq | 1p4c | 10495 | 7.08× | 9 |
