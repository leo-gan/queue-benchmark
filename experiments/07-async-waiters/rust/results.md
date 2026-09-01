# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | 1p32c | 712608 | 1.00× | 9 |
| steal-deque | 1p32c | 761181 | 1.07× | 9 |
| crossbeam-channel | 1p32c | 813558 | 1.14× | 9 |
