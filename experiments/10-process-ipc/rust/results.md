# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 6283 | 1.00× | 9 |
| steal-deque | bytes | 6324 | 1.01× | 9 |
| tokio-mpsc | bytes | 8173 | 1.30× | 9 |
| std-mpsc | bytes | 8748 | 1.39× | 9 |
| crossbeam-channel | bytes | 9527 | 1.52× | 9 |
| flume | bytes | 9595 | 1.53× | 9 |
| async-channel | bytes | 13657 | 2.17× | 9 |
| pipe-ipc | bytes | 579945 | 92.30× | 9 |
