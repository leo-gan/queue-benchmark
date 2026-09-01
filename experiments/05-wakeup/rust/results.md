# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| std-mpsc | bytes | 112442180 | 1.00× | 9 |
| crossbeam-channel | bytes | 115198938 | 1.02× | 9 |
| steal-deque | bytes | 116519419 | 1.04× | 9 |
| tokio-mpsc | bytes | 116829496 | 1.04× | 9 |
| crossbeam-queue | bytes | 117552237 | 1.05× | 9 |
