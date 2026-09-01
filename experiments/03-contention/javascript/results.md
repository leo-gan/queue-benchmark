# javascript

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| fastq | 4p4c | 1631 | 1.00× | 9 |
| fastq | 4p1c | 2002 | 1.23× | 9 |
| steal-deque | 4p4c | 2753 | 1.69× | 9 |
| steal-deque | 4p1c | 6944 | 4.26× | 9 |
| fastq | 1p4c | 8377 | 5.14× | 9 |
| steal-deque | 1p4c | 9252 | 5.67× | 9 |
