# Experiment plan

One question per folder. Never compare times across languages. Group libraries
by relative handoff time vs the fastest on that sample. Do not crown a winner.

| # | Folder | Status | Question |
|---|--------|--------|----------|
| 1 | [01-spsc-handoff](01-spsc-handoff/) | Ready | SPSC handoff of a small message |
| 2 | [02-payload-size](02-payload-size/) | Ready | Same SPSC, 4 KiB payload |
| 3 | [03-contention](03-contention/) | Ready | 1P4C / 4P1C / 4P4C |
| 4 | [04-backpressure](04-backpressure/) | Ready | Bounded queue, slow consumer |
| 5 | [05-wakeup](05-wakeup/) | Ready | Empty-queue wake latency |
| 6 | [06-burst](06-burst/) | Ready | Burst fill then drain |
| 7 | [07-async-waiters](07-async-waiters/) | Ready | Many async waiters |
| 8 | [08-async-backpressure](08-async-backpressure/) | Ready | Bounded async put |
| 9 | [09-async-cancel](09-async-cancel/) | Ready | Cancel parked async getters |
| 10 | [10-process-ipc](10-process-ipc/) | Ready | Category P vs in-process |
| 11 | [11-shared-memory](11-shared-memory/) | Ready | Category S ring |
| 12 | [12-durable-local](12-durable-local/) | Ready | Category D sqlite |

T1=01, T2=02, T3=03, T4=04, T5=05, T6=06, A2=07, A3=08, A4=09.
P/S/D have Python runners only. Do not plot P/S/D next to T.
