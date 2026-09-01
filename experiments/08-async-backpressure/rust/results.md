# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 6674 | 1.00× | 9 |
| crossbeam-queue | bytes | 6748 | 1.01× | 9 |
| tokio-mpsc | bytes | 8924 | 1.34× | 9 |
| std-mpsc | bytes | 8977 | 1.35× | 9 |
| crossbeam-channel | bytes | 9430 | 1.41× | 9 |
| flume | bytes | 9457 | 1.42× | 9 |
| async-channel | bytes | 14253 | 2.14× | 9 |
