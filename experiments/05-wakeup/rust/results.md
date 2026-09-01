# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| flume | bytes | 108275696 | 1.00× | 9 |
| crossbeam-channel | bytes | 110878229 | 1.02× | 9 |
| std-mpsc | bytes | 112953182 | 1.04× | 9 |
| crossbeam-queue | bytes | 113121761 | 1.04× | 9 |
| tokio-mpsc | bytes | 115180605 | 1.06× | 9 |
| async-channel | bytes | 116934849 | 1.08× | 9 |
| steal-deque | bytes | 119233013 | 1.10× | 9 |
