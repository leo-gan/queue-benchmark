# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 6105 | 1.00× | 9 |
| steal-deque | bytes | 6124 | 1.00× | 9 |
| crossbeam-channel | bytes | 6962 | 1.14× | 9 |
| tokio-mpsc | bytes | 7671 | 1.26× | 9 |
| std-mpsc | bytes | 7690 | 1.26× | 9 |
