# Benchmark design

How this lab is organized: **communication category first**, then
implementation family, then workload. Rankings are never global.

The [category plan](../internal/CATEGORY_BENCHMARK_PLAN.md) is the source
of truth for the rollout. This page is the published methodology.

## Comparison boundary

Compare queues **inside one language and one communication category**.

| ID | Category | What the queue crosses | Published |
|----|----------|------------------------|-----------|
| **T** | Thread / in-process | OS threads in one process | Yes |
| **A** | Async / event-loop | Tasks on one event loop | Yes |
| **P** | Process / IPC | Processes + serialization | Python opt-in (exp. 10) |
| **S** | Shared memory | Processes + mapped bytes | Python opt-in (exp. 11) |
| **D** | Durable / local disk | Process + fsync / WAL | Python opt-in (exp. 12) |
| **N** | Local broker | Client + localhost server | Separate system report |

A locked deque and an async channel answer different questions. A
localhost Redis row is a **system** measurement, not a data-structure
measurement. Do not put it on the same chart as `deque-lock`.

Implementation family (`locked`, `concurrent`, `spsc`, `work-stealing`,
`scheduler`) is a **label** inside a category. It is not a license to
mix T with A.

Properties that are **not** categories: bounded vs unbounded, FIFO vs
priority, blocking vs spin vs yield, SPSC vs MPMC.

## Patterns (CSV `Pattern`)

| CSV value | Say this | What actually ran |
|-----------|----------|-------------------|
| `bytes` | **SPSC** | One producer, one consumer |
| `stream` | **MPMC** | Two producers, two consumers |
| `1p4c` / `4p1c` / `4p4c` | Named P×C | Default full matrix + experiment 3 |

There is no stream I/O in this suite. In-process queues move already-built
payloads. If a library cannot do MPMC, **skip the cell** — do not fake it
with a mutex around an SPSC structure.

## What we time

See [Timing honesty](TIMING_HONESTY.md) and [Architecture](architecture.md).

1. Prepare (untimed): construct the queue, allocate payloads, spawn workers.
2. Timed loop: enqueue, dequeue, record handoff, check fidelity.
3. Warmup index `0` stays in the CSV; analysis drops it.

**Primary metrics**

| Metric | Why |
|--------|-----|
| Completed handoffs / s | Producer-only put/s can lie |
| Enqueue ns (`TimeEnq`) | Produce cost |
| Dequeue ns (`TimeDeq`) | Consume cost |
| Handoff ns (`TimeHandoff`) | End-to-end; default rank |
| p50 / p99 / p99.9 (`handoff_p999_ns`) | Tail matters more than the mean |
| Peak RSS | Retention after drain |
| Messages / CPU-second (`msgs_per_cpu_sec`) | Spin can “win” latency and burn cores; needs `CpuTimeNs` |
| Fidelity | Lost or duplicated items are errors, not speed |

## Published matrix (now)

Same run modes as [Modes](modes.md): smoke / all-single / full / research.

| Axis | Now |
|------|-----|
| Languages | C, C#, JavaScript, Python, Rust |
| Categories | T and A on the default matrix; P/S/D opt-in (see [categories](queue_categories.md)) |
| Pattern | SPSC, 2P2C, 1P4C, 4P1C, 4P4C (skip if the library cannot) |
| Payloads | `message`, `document`, `telemetry`, `strings`, `event` |
| Experiments | [01](../experiments/01-spsc-handoff/)–[12](../experiments/12-durable-local/) |

## Designed tests

### Category T

| ID | Question | Shipped? |
|----|----------|----------|
| T1 | 1P1C, small payload — baseline overhead | Experiment 1 |
| T2 | Does ranking flip at 4 KiB? | Experiment 2 |
| T3 | 1P4C / 4P1C / 4P4C contention | Experiment 3 |
| T4 | Bounded queue, slow consumer (backpressure) | Experiment 4 |
| T5 | Empty-queue wakeup latency | Experiment 5 |
| T6 | Burst, then drain | Experiment 6 |

### Category A

Same SPSC/MPMC cells as T, but the workers are async tasks. Extra tests:
experiment 7 (many waiters), 8 (bounded async), 9 (cancel). Do not rank an
A library against a T library.

### Categories P, S, D

Python runners exist (opt-in, not in the default matrix):

- P: `multiprocessing.Queue` / `multiprocessing.SimpleQueue` — experiment 10
- S: `shared-ring` — experiment 11
- D: `sqlite-queue` — experiment 12

They never share a violin with T.

The dashboard **Category** filter is Thread / Async / Process / Shared /
Durable / Other. P, S, and D series come from the Python opt-in runners
and never share a violin with T. Other is schedulers (JavaScript
`p-queue`).

## What a single computer can measure

Reliable: throughput, latency tails, thread/task scaling up to core count,
backpressure, wakeup, burst, payload size, fidelity, CPU, RSS.

Not this lab: multi-node brokers, WAN, cross-socket NUMA unless the box
is multi-socket and the run says so.

## How to read a result

1. Pick a **language**.
2. Pick a **category** (T or A) in the dashboard Category control.
3. Pick a **pattern** (SPSC or MPMC) and a **payload**.
4. Compare families inside that slice.

There is no overall score. A queue that wins T1 can lose T2 or T4.

See [Comparison rules](COMPARISON_RULES.md) for the hard “never” list.
