# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 8443 | 1.00× | 9 |
| std-mpsc | bytes | 8655 | 1.03× | 9 |
| crossbeam-channel | bytes | 9586 | 1.14× | 9 |
| tokio-mpsc | bytes | 10666 | 1.26× | 9 |
