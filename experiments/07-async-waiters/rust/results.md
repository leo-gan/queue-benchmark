# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| async-channel | 1p32c | 58806 | 1.00× | 9 |
| crossbeam-queue | 1p32c | 537432 | 9.14× | 9 |
| steal-deque | 1p32c | 548143 | 9.32× | 9 |
| flume | 1p32c | 697096 | 11.85× | 9 |
| crossbeam-channel | 1p32c | 714140 | 12.14× | 9 |
