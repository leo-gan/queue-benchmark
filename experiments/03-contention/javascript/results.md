# javascript

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| fastq | 4p4c | 1708 | 1.00× | 9 |
| fastq | 4p1c | 2471 | 1.45× | 9 |
| steal-deque | 4p4c | 2791 | 1.63× | 9 |
| steal-deque | 4p1c | 7167 | 4.20× | 9 |
| fastq | 1p4c | 8809 | 5.16× | 9 |
| steal-deque | 1p4c | 9910 | 5.80× | 9 |
