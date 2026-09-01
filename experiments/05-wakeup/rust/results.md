# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 107065715 | 1.00× | 9 |
| tokio-mpsc | bytes | 107391680 | 1.00× | 9 |
| std-mpsc | bytes | 111258515 | 1.04× | 9 |
| steal-deque | bytes | 111756583 | 1.04× | 9 |
| crossbeam-channel | bytes | 113484046 | 1.06× | 9 |
