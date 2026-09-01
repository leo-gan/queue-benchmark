# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 69104 | 1.00× | 9 |
| steal-deque | bytes | 71219 | 1.03× | 9 |
| crossbeam-channel | bytes | 87305 | 1.26× | 9 |
| tokio-mpsc | bytes | 88989 | 1.29× | 9 |
| std-mpsc | bytes | 126398 | 1.83× | 9 |
