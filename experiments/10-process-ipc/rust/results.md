# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 5918 | 1.00× | 9 |
| steal-deque | bytes | 6569 | 1.11× | 9 |
| crossbeam-channel | bytes | 6800 | 1.15× | 9 |
| std-mpsc | bytes | 6981 | 1.18× | 9 |
| tokio-mpsc | bytes | 7547 | 1.28× | 9 |
| pipe-ipc | bytes | 708537 | 119.73× | 9 |
