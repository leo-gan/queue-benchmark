# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 15511 | 1.00× | 9 |
| crossbeam-queue | bytes | 15892 | 1.02× | 9 |
| crossbeam-channel | bytes | 16754 | 1.08× | 9 |
| tokio-mpsc | bytes | 17205 | 1.11× | 9 |
| std-mpsc | bytes | 18020 | 1.16× | 9 |
