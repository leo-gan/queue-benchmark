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
| **P** | Process / IPC | Processes + serialization | When a runner exists |
| **S** | Shared memory | Processes + mapped bytes | When a runner exists |
| **D** | Durable / local disk | Process + fsync / WAL | When a runner exists |
| **N** | Local broker | Client + localhost server | Separate system report |

A locked deque and an async channel answer different questions. A
localhost Redis row is a **system** measurement, not a data-structure
measurement. Do not put it on the same chart as `deque-lock`.

Implementation family (`locked`, `concurrent`, `spsc`, `scheduler`) is a
**label** inside a category. It is not a license to mix T with A.

Properties that are **not** categories: bounded vs unbounded, FIFO vs
priority, blocking vs spin vs yield, SPSC vs MPMC.

## Patterns (CSV `StringOrStream`)

The CSV still uses serializer-benchmark names so analysis stays reusable.

| CSV value | Say this | What actually ran |
|-----------|----------|-------------------|
| `bytes` | **SPSC** | One producer, one consumer |
| `stream` | **MPMC** | Two producers, two consumers |

There is no stream I/O in this suite. In-process queues move already-built
payloads. If a library cannot do MPMC, **skip the cell** — do not fake it
with a mutex around an SPSC structure.

Planned (not shipped): 1P4C, 4P1C, 4P4C as their own experiment questions.

## What we time

See [Timing honesty](TIMING_HONESTY.md) and [Architecture](architecture.md).

1. Prepare (untimed): construct the queue, allocate payloads, spawn workers.
2. Timed loop: enqueue, dequeue, record handoff, check fidelity.
3. Warmup index `0` stays in the CSV; analysis drops it.

**Primary metrics**

| Metric | Why |
|--------|-----|
| Completed handoffs / s | Producer-only put/s can lie |
| Enqueue ns (`TimeSer`) | Produce cost |
| Dequeue ns (`TimeDeser`) | Consume cost |
| Handoff ns (`TimeSerAndDeser`) | End-to-end; default rank |
| p50 / p99 (p99.9 in `full`) | Tail matters more than the mean |
| Peak RSS | Retention after drain |
| Messages / CPU-second | Spin can “win” latency and burn cores |
| Fidelity | Lost or duplicated items are errors, not speed |

## Published matrix (now)

Same run modes as [Modes](modes.md): smoke / all-single / full / research.

| Axis | Now |
|------|-----|
| Languages | C, C#, JavaScript, Python, Rust |
| Categories | T and A (see [categories](queue_categories.md)) |
| Pattern | SPSC required; MPMC if the library supports it |
| Payloads | `message`, `document`, `telemetry`, `strings`, `event` |
| Experiments | [01 SPSC handoff](../experiments/01-spsc-handoff/), [02 payload size](../experiments/02-payload-size/) |

## Designed tests (not all shipped)

### Category T

| ID | Question | Shipped? |
|----|----------|----------|
| T1 | 1P1C, small payload — baseline overhead | Experiment 1 |
| T2 | Does ranking flip at 4 KiB? | Experiment 2 |
| T3 | 1P4C / 4P1C / 4P4C contention | No |
| T4 | Bounded queue, slow consumer (backpressure) | No |
| T5 | Empty-queue wakeup latency | No |
| T6 | Burst, then drain | No |

### Category A

Same SPSC/MPMC cells as T, but the workers are async tasks. Extra tests
(many waiters, cancel, loop lag) are not shipped. Do not rank an A library
against a T library.

### Categories P, S, D

Documented in [queue categories](queue_categories.md). No runner yet — no
numbers, no dashboard series, no experiment folder.

## What a single computer can measure

Reliable: throughput, latency tails, thread/task scaling up to core count,
backpressure, wakeup, burst, payload size, fidelity, CPU, RSS.

Not this lab: multi-node brokers, WAN, cross-socket NUMA unless the box
is multi-socket and the run says so.

## How to read a result

1. Pick a **language**.
2. Pick a **category** (T or A).
3. Pick a **pattern** (SPSC or MPMC) and a **payload**.
4. Compare families inside that slice.

There is no overall score. A queue that wins T1 can lose T2 or T4.
