# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | 4p1c | 85746 | 1.00× | 9 |
| crossbeam-queue | 1p4c | 92958 | 1.08× | 9 |
| crossbeam-channel | 4p1c | 94232 | 1.10× | 9 |
| crossbeam-channel | 1p4c | 113390 | 1.32× | 9 |
| crossbeam-channel | 4p4c | 121878 | 1.42× | 9 |
| crossbeam-queue | 4p4c | 122294 | 1.43× | 9 |
