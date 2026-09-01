# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | 1p4c | 83419 | 1.00× | 9 |
| crossbeam-channel | 1p4c | 87192 | 1.05× | 9 |
| crossbeam-channel | 4p1c | 87770 | 1.05× | 9 |
| crossbeam-queue | 1p4c | 89003 | 1.07× | 9 |
| steal-deque | 4p1c | 94893 | 1.14× | 9 |
| crossbeam-queue | 4p1c | 97062 | 1.16× | 9 |
| crossbeam-queue | 4p4c | 122551 | 1.47× | 9 |
| steal-deque | 4p4c | 123782 | 1.48× | 9 |
| crossbeam-channel | 4p4c | 128791 | 1.54× | 9 |
