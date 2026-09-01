# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 70643 | 1.00× | 9 |
| crossbeam-queue | bytes | 71844 | 1.02× | 9 |
| crossbeam-channel | bytes | 89987 | 1.27× | 9 |
| tokio-mpsc | bytes | 90917 | 1.29× | 9 |
| std-mpsc | bytes | 128345 | 1.82× | 9 |
