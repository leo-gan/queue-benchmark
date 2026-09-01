# javascript

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| fastq | 4p4c | 1547 | 1.00× | 9 |
| fastq | 4p1c | 2663 | 1.72× | 9 |
| steal-deque | 4p4c | 7424 | 4.80× | 9 |
| steal-deque | 4p1c | 8819 | 5.70× | 9 |
| steal-deque | 1p4c | 11802 | 7.63× | 9 |
| fastq | 1p4c | 12187 | 7.88× | 9 |
