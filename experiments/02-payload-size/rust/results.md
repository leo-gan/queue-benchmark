# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 23655 | 1.00× | 9 |
| crossbeam-queue | bytes | 23724 | 1.00× | 9 |
| flume | bytes | 25398 | 1.07× | 9 |
| crossbeam-channel | bytes | 25687 | 1.09× | 9 |
| std-mpsc | bytes | 26719 | 1.13× | 9 |
| tokio-mpsc | bytes | 28938 | 1.22× | 9 |
| async-channel | bytes | 32443 | 1.37× | 9 |
