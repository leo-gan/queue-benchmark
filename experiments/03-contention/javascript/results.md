# javascript

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| fastq | 4p4c | 1515 | 1.00× | 9 |
| fastq | 4p1c | 2254 | 1.49× | 9 |
| steal-deque | 4p4c | 2819 | 1.86× | 9 |
| steal-deque | 4p1c | 7234 | 4.77× | 9 |
| steal-deque | 1p4c | 8983 | 5.93× | 9 |
| fastq | 1p4c | 12172 | 8.03× | 9 |
