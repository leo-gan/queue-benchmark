# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| tokio-mpsc | bytes | 115273182 | 1.00× | 9 |
| std-mpsc | bytes | 115557439 | 1.00× | 9 |
| crossbeam-queue | bytes | 116354279 | 1.01× | 9 |
| crossbeam-channel | bytes | 117627514 | 1.02× | 9 |
| steal-deque | bytes | 117765082 | 1.02× | 9 |
