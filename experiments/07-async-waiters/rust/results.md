# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| async-channel | 1p32c | 54825 | 1.00× | 9 |
| crossbeam-channel | 1p32c | 623469 | 11.37× | 9 |
| flume | 1p32c | 654390 | 11.94× | 9 |
| crossbeam-queue | 1p32c | 690555 | 12.60× | 9 |
| steal-deque | 1p32c | 753233 | 13.74× | 9 |
