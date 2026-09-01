# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| async-channel | 4p1c | 27763 | 1.00× | 9 |
| async-channel | 4p4c | 49717 | 1.79× | 9 |
| flume | 4p1c | 77956 | 2.81× | 9 |
| steal-deque | 4p1c | 79808 | 2.87× | 9 |
| crossbeam-queue | 4p1c | 88352 | 3.18× | 9 |
| flume | 1p4c | 90483 | 3.26× | 9 |
| crossbeam-channel | 4p1c | 91326 | 3.29× | 9 |
| async-channel | 1p4c | 93632 | 3.37× | 9 |
| steal-deque | 1p4c | 95966 | 3.46× | 9 |
| crossbeam-channel | 1p4c | 99882 | 3.60× | 9 |
| crossbeam-queue | 1p4c | 117056 | 4.22× | 9 |
| steal-deque | 4p4c | 140050 | 5.04× | 9 |
| crossbeam-channel | 4p4c | 143464 | 5.17× | 9 |
| crossbeam-queue | 4p4c | 156229 | 5.63× | 9 |
| flume | 4p4c | 159027 | 5.73× | 9 |
