# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 111462344 | 1.00× | 9 |
| std-mpsc | bytes | 112884971 | 1.01× | 9 |
| crossbeam-channel | bytes | 114432891 | 1.03× | 9 |
| steal-deque | bytes | 114938460 | 1.03× | 9 |
| flume | bytes | 115049308 | 1.03× | 9 |
| tokio-mpsc | bytes | 115475873 | 1.04× | 9 |
| async-channel | bytes | 116638464 | 1.05× | 9 |
