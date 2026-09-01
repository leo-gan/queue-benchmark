# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 8212 | 1.00× | 9 |
| crossbeam-queue | bytes | 8963 | 1.09× | 9 |
| std-mpsc | bytes | 9169 | 1.12× | 9 |
| crossbeam-channel | bytes | 9486 | 1.16× | 9 |
| flume | bytes | 10061 | 1.23× | 9 |
| tokio-mpsc | bytes | 10793 | 1.31× | 9 |
| async-channel | bytes | 16398 | 2.00× | 9 |
