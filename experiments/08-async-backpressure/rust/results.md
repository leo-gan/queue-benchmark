# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 8371 | 1.00× | 9 |
| std-mpsc | bytes | 9335 | 1.12× | 9 |
| crossbeam-channel | bytes | 9520 | 1.14× | 9 |
| tokio-mpsc | bytes | 10263 | 1.23× | 9 |
