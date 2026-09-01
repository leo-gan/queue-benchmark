# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 7826 | 1.00× | 9 |
| steal-deque | bytes | 7953 | 1.02× | 9 |
| std-mpsc | bytes | 8694 | 1.11× | 9 |
| flume | bytes | 9284 | 1.19× | 9 |
| crossbeam-channel | bytes | 9294 | 1.19× | 9 |
| tokio-mpsc | bytes | 10455 | 1.34× | 9 |
| async-channel | bytes | 16005 | 2.05× | 9 |
