# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 5821 | 1.00× | 9 |
| crossbeam-queue | bytes | 5915 | 1.02× | 9 |
| crossbeam-channel | bytes | 7201 | 1.24× | 9 |
| tokio-mpsc | bytes | 7511 | 1.29× | 9 |
| std-mpsc | bytes | 9747 | 1.67× | 9 |
