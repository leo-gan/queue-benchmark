# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | 4p1c | 75902 | 1.00× | 9 |
| crossbeam-channel | 4p1c | 85491 | 1.13× | 9 |
| crossbeam-queue | 4p1c | 89253 | 1.18× | 9 |
| crossbeam-queue | 1p4c | 94295 | 1.24× | 9 |
| crossbeam-channel | 1p4c | 94338 | 1.24× | 9 |
| steal-deque | 4p4c | 126458 | 1.67× | 9 |
| crossbeam-queue | 4p4c | 156891 | 2.07× | 9 |
| steal-deque | 1p4c | 163860 | 2.16× | 9 |
| crossbeam-channel | 4p4c | 176511 | 2.33× | 9 |
