# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| async-channel | bytes | 115417768 | 1.00× | 9 |
| flume | bytes | 115623111 | 1.00× | 9 |
| steal-deque | bytes | 116052890 | 1.01× | 9 |
| crossbeam-queue | bytes | 116261271 | 1.01× | 9 |
| std-mpsc | bytes | 116841472 | 1.01× | 9 |
| crossbeam-channel | bytes | 117291623 | 1.02× | 9 |
| tokio-mpsc | bytes | 118260930 | 1.02× | 9 |
