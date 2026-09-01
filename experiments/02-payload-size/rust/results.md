# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | bytes | 13782 | 1.00× | 9 |
| crossbeam-queue | bytes | 14313 | 1.04× | 9 |
| crossbeam-channel | bytes | 26832 | 1.95× | 9 |
| tokio-mpsc | bytes | 27065 | 1.96× | 9 |
| std-mpsc | bytes | 27430 | 1.99× | 9 |
