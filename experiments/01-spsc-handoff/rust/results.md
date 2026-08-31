# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 6337 | 1.00× | 9 |
| crossbeam-channel | bytes | 10001 | 1.58× | 9 |
| tokio-mpsc | bytes | 10732 | 1.69× | 9 |
| std-mpsc | bytes | 11019 | 1.74× | 9 |
