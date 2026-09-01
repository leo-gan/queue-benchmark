# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| async-channel | 1p32c | 48327 | 1.00× | 9 |
| steal-deque | 1p32c | 576311 | 11.93× | 9 |
| crossbeam-queue | 1p32c | 591312 | 12.24× | 9 |
| flume | 1p32c | 592306 | 12.26× | 9 |
| crossbeam-channel | 1p32c | 694136 | 14.36× | 9 |
