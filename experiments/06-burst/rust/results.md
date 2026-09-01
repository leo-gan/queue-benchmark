# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 72209 | 1.00× | 9 |
| crossbeam-queue | bytes | 75483 | 1.05× | 9 |
| std-mpsc | bytes | 119530 | 1.66× | 9 |
| flume | bytes | 120577 | 1.67× | 9 |
| tokio-mpsc | bytes | 124245 | 1.72× | 9 |
| crossbeam-channel | bytes | 126215 | 1.75× | 9 |
| async-channel | bytes | 178165 | 2.47× | 9 |
