# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | bytes | 25702 | 1.00× | 9 |
| crossbeam-channel | bytes | 26779 | 1.04× | 9 |
| std-mpsc | bytes | 27362 | 1.06× | 9 |
| tokio-mpsc | bytes | 28802 | 1.12× | 9 |
