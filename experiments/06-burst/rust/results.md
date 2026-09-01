# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 69444 | 1.00× | 9 |
| crossbeam-queue | bytes | 71154 | 1.02× | 9 |
| std-mpsc | bytes | 80418 | 1.16× | 9 |
| flume | bytes | 83572 | 1.20× | 9 |
| crossbeam-channel | bytes | 87303 | 1.26× | 9 |
| tokio-mpsc | bytes | 88253 | 1.27× | 9 |
| async-channel | bytes | 136672 | 1.97× | 9 |
