# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 5499 | 1.00× | 9 |
| crossbeam-queue | bytes | 5650 | 1.03× | 9 |
| std-mpsc | bytes | 6442 | 1.17× | 9 |
| flume | bytes | 7253 | 1.32× | 9 |
| tokio-mpsc | bytes | 7357 | 1.34× | 9 |
| crossbeam-channel | bytes | 7413 | 1.35× | 9 |
| async-channel | bytes | 12305 | 2.24× | 9 |
| pipe-ipc | bytes | 556888 | 101.27× | 9 |
