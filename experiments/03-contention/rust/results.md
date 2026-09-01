# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| async-channel | 4p1c | 27508 | 1.00× | 9 |
| async-channel | 1p4c | 37583 | 1.37× | 9 |
| async-channel | 4p4c | 43189 | 1.57× | 9 |
| crossbeam-queue | 4p1c | 92174 | 3.35× | 9 |
| flume | 1p4c | 94728 | 3.44× | 9 |
| steal-deque | 4p1c | 95851 | 3.48× | 9 |
| flume | 4p1c | 104537 | 3.80× | 9 |
| steal-deque | 1p4c | 104931 | 3.81× | 9 |
| crossbeam-queue | 1p4c | 112786 | 4.10× | 9 |
| flume | 4p4c | 124214 | 4.52× | 9 |
| steal-deque | 4p4c | 124402 | 4.52× | 9 |
| crossbeam-queue | 4p4c | 126386 | 4.59× | 9 |
| crossbeam-channel | 4p1c | 126562 | 4.60× | 9 |
| crossbeam-channel | 4p4c | 146551 | 5.33× | 9 |
| crossbeam-channel | 1p4c | 163372 | 5.94× | 9 |
