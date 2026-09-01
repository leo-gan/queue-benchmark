# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 8017 | 1.00× | 9 |
| crossbeam-queue | bytes | 8157 | 1.02× | 9 |
| std-mpsc | bytes | 8868 | 1.11× | 9 |
| crossbeam-channel | bytes | 9104 | 1.14× | 9 |
| flume | bytes | 9173 | 1.14× | 9 |
| tokio-mpsc | bytes | 10652 | 1.33× | 9 |
| async-channel | bytes | 16573 | 2.07× | 9 |
| pipe-ipc | bytes | 787457 | 98.22× | 9 |
