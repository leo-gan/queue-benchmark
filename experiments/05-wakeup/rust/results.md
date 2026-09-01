# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| async-channel | bytes | 114435033 | 1.00× | 9 |
| steal-deque | bytes | 115223085 | 1.01× | 9 |
| crossbeam-queue | bytes | 115340522 | 1.01× | 9 |
| flume | bytes | 115552494 | 1.01× | 9 |
| tokio-mpsc | bytes | 115868803 | 1.01× | 9 |
| std-mpsc | bytes | 116126463 | 1.01× | 9 |
| crossbeam-channel | bytes | 116398662 | 1.02× | 9 |
