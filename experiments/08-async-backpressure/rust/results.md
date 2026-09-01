# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 6606 | 1.00× | 9 |
| steal-deque | bytes | 6720 | 1.02× | 9 |
| crossbeam-channel | bytes | 9478 | 1.43× | 9 |
| std-mpsc | bytes | 10001 | 1.51× | 9 |
| tokio-mpsc | bytes | 11071 | 1.68× | 9 |
