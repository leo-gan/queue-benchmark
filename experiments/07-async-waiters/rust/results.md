# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| steal-deque | 1p32c | 626710 | 1.00× | 9 |
| crossbeam-channel | 1p32c | 735159 | 1.17× | 9 |
| crossbeam-queue | 1p32c | 756458 | 1.21× | 9 |
