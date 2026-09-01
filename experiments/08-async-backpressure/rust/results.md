# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 8013 | 1.00× | 9 |
| steal-deque | bytes | 8025 | 1.00× | 9 |
| std-mpsc | bytes | 8699 | 1.09× | 9 |
| flume | bytes | 9567 | 1.19× | 9 |
| crossbeam-channel | bytes | 9635 | 1.20× | 9 |
| tokio-mpsc | bytes | 10536 | 1.31× | 9 |
| async-channel | bytes | 16134 | 2.01× | 9 |
