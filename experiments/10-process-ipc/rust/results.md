# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 6101 | 1.00× | 9 |
| crossbeam-queue | bytes | 6947 | 1.14× | 9 |
| crossbeam-channel | bytes | 7286 | 1.19× | 9 |
| std-mpsc | bytes | 7822 | 1.28× | 9 |
| tokio-mpsc | bytes | 9544 | 1.56× | 9 |
| pipe-ipc | bytes | 581349 | 95.29× | 9 |
