# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 8159 | 1.00× | 9 |
| crossbeam-queue | bytes | 8462 | 1.04× | 9 |
| crossbeam-channel | bytes | 9471 | 1.16× | 9 |
| std-mpsc | bytes | 10036 | 1.23× | 9 |
| tokio-mpsc | bytes | 10935 | 1.34× | 9 |
