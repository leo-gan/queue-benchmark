# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 6341 | 1.00× | 9 |
| steal-deque | bytes | 6372 | 1.00× | 9 |
| crossbeam-channel | bytes | 7940 | 1.25× | 9 |
| tokio-mpsc | bytes | 8169 | 1.29× | 9 |
| std-mpsc | bytes | 8825 | 1.39× | 9 |
