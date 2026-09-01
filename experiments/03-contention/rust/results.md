# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| async-channel | 4p1c | 25178 | 1.00× | 9 |
| async-channel | 1p4c | 39389 | 1.56× | 9 |
| async-channel | 4p4c | 43144 | 1.71× | 9 |
| crossbeam-channel | 4p1c | 78889 | 3.13× | 9 |
| steal-deque | 4p1c | 82226 | 3.27× | 9 |
| flume | 4p1c | 85579 | 3.40× | 9 |
| flume | 1p4c | 86008 | 3.42× | 9 |
| crossbeam-queue | 4p1c | 86413 | 3.43× | 9 |
| steal-deque | 1p4c | 94573 | 3.76× | 9 |
| crossbeam-queue | 1p4c | 97595 | 3.88× | 9 |
| crossbeam-channel | 1p4c | 121339 | 4.82× | 9 |
| flume | 4p4c | 126264 | 5.01× | 9 |
| crossbeam-queue | 4p4c | 127290 | 5.06× | 9 |
| steal-deque | 4p4c | 129610 | 5.15× | 9 |
| crossbeam-channel | 4p4c | 129869 | 5.16× | 9 |
