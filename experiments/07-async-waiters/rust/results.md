# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| async-channel | 1p32c | 46115 | 1.00× | 9 |
| crossbeam-queue | 1p32c | 574440 | 12.46× | 9 |
| flume | 1p32c | 579843 | 12.57× | 9 |
| steal-deque | 1p32c | 598787 | 12.98× | 9 |
| crossbeam-channel | 1p32c | 638125 | 13.84× | 9 |
