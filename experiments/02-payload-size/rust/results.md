# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 14112 | 1.00× | 9 |
| crossbeam-queue | bytes | 15387 | 1.09× | 9 |
| flume | bytes | 16219 | 1.15× | 9 |
| crossbeam-channel | bytes | 17434 | 1.24× | 9 |
| tokio-mpsc | bytes | 17694 | 1.25× | 9 |
| async-channel | bytes | 22190 | 1.57× | 9 |
| std-mpsc | bytes | 27509 | 1.95× | 9 |
