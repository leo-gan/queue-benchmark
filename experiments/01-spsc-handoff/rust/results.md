# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 5907 | 1.00× | 9 |
| crossbeam-queue | bytes | 6081 | 1.03× | 9 |
| crossbeam-channel | bytes | 9184 | 1.55× | 9 |
| std-mpsc | bytes | 9628 | 1.63× | 9 |
| tokio-mpsc | bytes | 11009 | 1.86× | 9 |
