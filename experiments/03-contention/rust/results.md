# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| async-channel | 4p1c | 28074 | 1.00× | 9 |
| async-channel | 4p4c | 53470 | 1.90× | 9 |
| async-channel | 1p4c | 58001 | 2.07× | 9 |
| steal-deque | 4p1c | 77175 | 2.75× | 9 |
| flume | 4p1c | 78567 | 2.80× | 9 |
| crossbeam-queue | 4p1c | 78664 | 2.80× | 9 |
| crossbeam-channel | 4p1c | 96141 | 3.42× | 9 |
| flume | 1p4c | 102476 | 3.65× | 9 |
| crossbeam-queue | 1p4c | 106588 | 3.80× | 9 |
| crossbeam-channel | 1p4c | 114931 | 4.09× | 9 |
| steal-deque | 1p4c | 140146 | 4.99× | 9 |
| crossbeam-channel | 4p4c | 142295 | 5.07× | 9 |
| flume | 4p4c | 148533 | 5.29× | 9 |
| steal-deque | 4p4c | 153225 | 5.46× | 9 |
| crossbeam-queue | 4p4c | 162606 | 5.79× | 9 |
