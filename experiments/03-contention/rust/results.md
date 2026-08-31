# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-channel | 1p4c | 85288 | 1.00× | 9 |
| crossbeam-queue | 1p4c | 86020 | 1.01× | 9 |
| crossbeam-queue | 4p1c | 86879 | 1.02× | 9 |
| crossbeam-channel | 4p1c | 111984 | 1.31× | 9 |
| crossbeam-queue | 4p4c | 147823 | 1.73× | 9 |
| crossbeam-channel | 4p4c | 172917 | 2.03× | 9 |
