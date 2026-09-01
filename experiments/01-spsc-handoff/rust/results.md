# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 7861 | 1.00× | 9 |
| crossbeam-queue | bytes | 7943 | 1.01× | 9 |
| std-mpsc | bytes | 9100 | 1.16× | 9 |
| crossbeam-channel | bytes | 9115 | 1.16× | 9 |
| flume | bytes | 9297 | 1.18× | 9 |
| tokio-mpsc | bytes | 10809 | 1.38× | 9 |
| async-channel | bytes | 16072 | 2.04× | 9 |
