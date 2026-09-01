# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 13326 | 1.00× | 9 |
| crossbeam-queue | bytes | 20491 | 1.54× | 9 |
| crossbeam-channel | bytes | 25758 | 1.93× | 9 |
| flume | bytes | 26131 | 1.96× | 9 |
| std-mpsc | bytes | 26181 | 1.96× | 9 |
| tokio-mpsc | bytes | 28052 | 2.11× | 9 |
| async-channel | bytes | 32566 | 2.44× | 9 |
