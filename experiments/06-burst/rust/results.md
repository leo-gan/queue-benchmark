# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 71176 | 1.00× | 9 |
| crossbeam-queue | bytes | 71737 | 1.01× | 9 |
| crossbeam-channel | bytes | 86437 | 1.21× | 9 |
| std-mpsc | bytes | 87162 | 1.22× | 9 |
| tokio-mpsc | bytes | 88325 | 1.24× | 9 |
