# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-channel | bytes | 25877 | 1.00× | 9 |
| std-mpsc | bytes | 26473 | 1.02× | 9 |
| crossbeam-queue | bytes | 26821 | 1.04× | 9 |
| tokio-mpsc | bytes | 29727 | 1.15× | 9 |
