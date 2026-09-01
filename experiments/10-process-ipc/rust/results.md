# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 5322 | 1.00× | 9 |
| steal-deque | bytes | 5617 | 1.06× | 9 |
| flume | bytes | 7115 | 1.34× | 9 |
| std-mpsc | bytes | 7147 | 1.34× | 9 |
| tokio-mpsc | bytes | 7170 | 1.35× | 9 |
| crossbeam-channel | bytes | 7626 | 1.43× | 9 |
| async-channel | bytes | 11749 | 2.21× | 9 |
| pipe-ipc | bytes | 614339 | 115.43× | 9 |
