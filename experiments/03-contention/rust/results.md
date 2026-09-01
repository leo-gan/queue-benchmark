# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | 1p4c | 71565 | 1.00× | 9 |
| crossbeam-queue | 4p1c | 82576 | 1.15× | 9 |
| crossbeam-channel | 4p1c | 89135 | 1.25× | 9 |
| crossbeam-queue | 1p4c | 100798 | 1.41× | 9 |
| steal-deque | 4p1c | 109344 | 1.53× | 9 |
| crossbeam-channel | 1p4c | 116097 | 1.62× | 9 |
| crossbeam-channel | 4p4c | 131463 | 1.84× | 9 |
| crossbeam-queue | 4p4c | 133917 | 1.87× | 9 |
| steal-deque | 4p4c | 134256 | 1.88× | 9 |
