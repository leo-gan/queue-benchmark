# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 68054 | 1.00× | 9 |
| crossbeam-queue | bytes | 68793 | 1.01× | 9 |
| tokio-mpsc | bytes | 83751 | 1.23× | 9 |
| crossbeam-channel | bytes | 87577 | 1.29× | 9 |
| std-mpsc | bytes | 94196 | 1.38× | 9 |
