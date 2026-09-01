# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 109714719 | 1.00× | 9 |
| std-mpsc | bytes | 110839695 | 1.01× | 9 |
| crossbeam-channel | bytes | 111755228 | 1.02× | 9 |
| tokio-mpsc | bytes | 113737765 | 1.04× | 9 |
| steal-deque | bytes | 114256233 | 1.04× | 9 |
