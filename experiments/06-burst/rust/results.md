# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 67915 | 1.00× | 9 |
| steal-deque | bytes | 68141 | 1.00× | 9 |
| flume | bytes | 80085 | 1.18× | 9 |
| tokio-mpsc | bytes | 84131 | 1.24× | 9 |
| crossbeam-channel | bytes | 84464 | 1.24× | 9 |
| std-mpsc | bytes | 86112 | 1.27× | 9 |
| async-channel | bytes | 131431 | 1.94× | 9 |
