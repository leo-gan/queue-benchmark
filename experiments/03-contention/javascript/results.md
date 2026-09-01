# javascript

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| fastq | 4p4c | 1674 | 1.00× | 9 |
| fastq | 4p1c | 2436 | 1.46× | 9 |
| steal-deque | 4p4c | 2872 | 1.72× | 9 |
| steal-deque | 4p1c | 7381 | 4.41× | 9 |
| steal-deque | 1p4c | 9423 | 5.63× | 9 |
| fastq | 1p4c | 9558 | 5.71× | 9 |
