# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 5696 | 1.00× | 9 |
| crossbeam-queue | bytes | 5766 | 1.01× | 9 |
| crossbeam-channel | bytes | 6964 | 1.22× | 9 |
| tokio-mpsc | bytes | 7447 | 1.31× | 9 |
| std-mpsc | bytes | 8590 | 1.51× | 9 |
