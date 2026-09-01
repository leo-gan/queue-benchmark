# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 12698 | 1.00× | 9 |
| crossbeam-queue | bytes | 12926 | 1.02× | 9 |
| crossbeam-channel | bytes | 13908 | 1.10× | 9 |
| std-mpsc | bytes | 14351 | 1.13× | 9 |
| tokio-mpsc | bytes | 15154 | 1.19× | 9 |
