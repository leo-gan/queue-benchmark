# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 13724 | 1.00× | 9 |
| crossbeam-queue | bytes | 14572 | 1.06× | 9 |
| crossbeam-channel | bytes | 16291 | 1.19× | 9 |
| tokio-mpsc | bytes | 16528 | 1.20× | 9 |
| std-mpsc | bytes | 17874 | 1.30× | 9 |
