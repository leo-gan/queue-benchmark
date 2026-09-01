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
| 13 | [13-payload-size-sweep](13-payload-size-sweep/) | Ready | Which payload sizes change SPSC ranking |

T1=01, T2=02, T3=03, T4=04, T5=05, T6=06, A2=07, A3=08, A4=09.
P/S/D have Python runners only. Do not plot P/S/D next to T.
Experiment 13 is a methodology question about the default matrix, not a new communication category.

## After Experiment 13

SPSC ranking is a **size** question, not a data-type question. Runners already
build opaque byte strings. The five published names are five lengths between
256 B and 4 KiB.

Sweep (1 B, 64 B, 256 B, 4 KiB, 64 KiB; n = 100; 99 trials after warmup):

- Python, C, C#, and JavaScript: the fastest queue stays the same at every
  size. Nearby libraries sometimes swap places by a nanosecond. Making the
  message larger does not make the handoff much slower, because these
  queues store a short reference to the bytes already in memory instead of
  copying every byte.
- Rust: 1 B and 64 B match 256 B. At 4 KiB the queues copy the bytes, so
  every library takes about nine times longer and they finish within about
  20 percent of each other. At 64 KiB the copy is so expensive that the
  small-message order reverses (Spearman −0.36, about 280 times slower).

**Default matrix: two sizes, 256 B (`message`) and 4 KiB (`document`).**
Drop `event` / `telemetry` / `strings`. Keep 64 KiB as this experiment, not
a third published type. Do not use item count 1 / 100 / 10000 as a substitute
for payload bytes.

The default run config now uses those two sizes (`size_256`, `size_4096`).
See the size-dimension follow-up on this branch.

Combined page: `experiments/13-payload-size-sweep/results.md`.
PR: https://github.com/leo-gan/queue-benchmark/pull/32
