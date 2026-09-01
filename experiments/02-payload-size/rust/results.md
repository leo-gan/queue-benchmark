# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 13434 | 1.00× | 9 |
| steal-deque | bytes | 13605 | 1.01× | 9 |
| std-mpsc | bytes | 28052 | 2.09× | 9 |
| tokio-mpsc | bytes | 29443 | 2.19× | 9 |
| flume | bytes | 30777 | 2.29× | 9 |
| crossbeam-channel | bytes | 32365 | 2.41× | 9 |
| async-channel | bytes | 34083 | 2.54× | 9 |
