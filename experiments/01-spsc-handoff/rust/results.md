# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 6791 | 1.00× | 9 |
| std-mpsc | bytes | 7463 | 1.10× | 9 |
| crossbeam-channel | bytes | 8273 | 1.22× | 9 |
| tokio-mpsc | bytes | 8604 | 1.27× | 9 |
