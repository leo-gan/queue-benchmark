# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 5408 | 1.00× | 9 |
| crossbeam-queue | bytes | 5454 | 1.01× | 9 |
| crossbeam-channel | bytes | 6734 | 1.25× | 9 |
| tokio-mpsc | bytes | 7144 | 1.32× | 9 |
| std-mpsc | bytes | 7785 | 1.44× | 9 |
| pipe-ipc | bytes | 566400 | 104.73× | 9 |
