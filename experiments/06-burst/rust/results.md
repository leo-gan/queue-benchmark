# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 67704 | 1.00× | 9 |
| steal-deque | bytes | 70298 | 1.04× | 9 |
| flume | bytes | 80440 | 1.19× | 9 |
| std-mpsc | bytes | 82899 | 1.22× | 9 |
| crossbeam-channel | bytes | 84134 | 1.24× | 9 |
| tokio-mpsc | bytes | 84272 | 1.24× | 9 |
| async-channel | bytes | 131617 | 1.94× | 9 |
