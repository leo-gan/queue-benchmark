# rust

| Library | Pattern | Median handoff (ns) | vs fastest | n |
|---------|---------|--------------------:|-----------:|--:|
| crossbeam-queue | 4p1c | 74459 | 1.00× | 9 |
| steal-deque | 4p1c | 75794 | 1.02× | 9 |
| crossbeam-queue | 1p4c | 95746 | 1.29× | 9 |
| crossbeam-channel | 4p1c | 96011 | 1.29× | 9 |
| crossbeam-channel | 1p4c | 102709 | 1.38× | 9 |
| crossbeam-queue | 4p4c | 118935 | 1.60× | 9 |
| crossbeam-channel | 4p4c | 126118 | 1.69× | 9 |
| steal-deque | 1p4c | 139148 | 1.87× | 9 |
| steal-deque | 4p4c | 146370 | 1.97× | 9 |
