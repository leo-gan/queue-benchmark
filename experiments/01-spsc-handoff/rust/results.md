# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 8244 | 1.00× | 9 |
| crossbeam-queue | bytes | 8535 | 1.04× | 9 |
| crossbeam-channel | bytes | 9624 | 1.17× | 9 |
| std-mpsc | bytes | 9698 | 1.18× | 9 |
| tokio-mpsc | bytes | 10543 | 1.28× | 9 |
