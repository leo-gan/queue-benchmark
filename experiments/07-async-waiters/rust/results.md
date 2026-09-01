# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | 1p32c | 564804 | 1.00× | 9 |
| steal-deque | 1p32c | 592309 | 1.05× | 9 |
| crossbeam-channel | 1p32c | 638716 | 1.13× | 9 |
