# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-channel | 1p32c | 711488 | 1.00× | 9 |
| steal-deque | 1p32c | 779024 | 1.09× | 9 |
| crossbeam-queue | 1p32c | 796799 | 1.12× | 9 |
