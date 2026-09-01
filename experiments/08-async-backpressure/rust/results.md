# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 5842 | 1.00× | 9 |
| crossbeam-queue | bytes | 5886 | 1.01× | 9 |
| tokio-mpsc | bytes | 7756 | 1.33× | 9 |
| std-mpsc | bytes | 9395 | 1.61× | 9 |
| flume | bytes | 9414 | 1.61× | 9 |
| crossbeam-channel | bytes | 9426 | 1.61× | 9 |
| async-channel | bytes | 12658 | 2.17× | 9 |
