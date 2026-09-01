# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 5996 | 1.00× | 9 |
| steal-deque | bytes | 6530 | 1.09× | 9 |
| crossbeam-channel | bytes | 7043 | 1.17× | 9 |
| std-mpsc | bytes | 7490 | 1.25× | 9 |
| tokio-mpsc | bytes | 7641 | 1.27× | 9 |
| pipe-ipc | bytes | 602397 | 100.47× | 9 |
