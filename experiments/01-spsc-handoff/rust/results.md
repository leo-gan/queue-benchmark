# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 7814 | 1.00× | 9 |
| crossbeam-queue | bytes | 8136 | 1.04× | 9 |
| std-mpsc | bytes | 9559 | 1.22× | 9 |
| flume | bytes | 9594 | 1.23× | 9 |
| crossbeam-channel | bytes | 9907 | 1.27× | 9 |
| tokio-mpsc | bytes | 10639 | 1.36× | 9 |
| async-channel | bytes | 16519 | 2.11× | 9 |
