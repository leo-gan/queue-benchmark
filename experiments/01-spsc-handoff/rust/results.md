# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 8511 | 1.00× | 9 |
| crossbeam-queue | bytes | 8639 | 1.02× | 9 |
| std-mpsc | bytes | 9192 | 1.08× | 9 |
| crossbeam-channel | bytes | 9456 | 1.11× | 9 |
| flume | bytes | 9585 | 1.13× | 9 |
| tokio-mpsc | bytes | 10831 | 1.27× | 9 |
| async-channel | bytes | 16811 | 1.98× | 9 |
