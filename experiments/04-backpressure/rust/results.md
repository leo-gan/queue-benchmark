# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 8442 | 1.00× | 9 |
| std-mpsc | bytes | 8820 | 1.04× | 9 |
| crossbeam-channel | bytes | 9477 | 1.12× | 9 |
| tokio-mpsc | bytes | 10697 | 1.27× | 9 |
