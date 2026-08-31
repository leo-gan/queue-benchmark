# Queue categories

Compare libraries **inside one language and one communication category**.
Implementation family is a label, not a separate leaderboard.

See [Benchmark design](BENCHMARK_DESIGN.md) for tests and metrics.

## Published: communication model

| ID | Category | What it is | In this repo |
|----|----------|------------|--------------|
| **T** | Thread / in-process | OS threads, one process | locked, concurrent, spsc-ring |
| **A** | Async / event-loop | Tasks on one loop | `asyncio.Queue`, `Channel`, `tokio-mpsc` |

A locked deque and an async channel answer different questions. Do not
rank them against each other.

### T — families (sub-labels)

| Family | What it is | Example |
|--------|------------|---------|
| **locked** | Mutex around a stdlib queue. Baseline. | Python `deque-lock`, C# `Queue+lock`, JS `Array`, C `mutex-queue` |
| **concurrent** | Thread-safe MPSC/MPMC | Python `queue.Queue`, C# `ConcurrentQueue`, Rust `crossbeam-channel`, JS `fastq` |
| **spsc** | Single-producer ring (no mutex on the happy path) | C `spsc-ring`, Python `spsc-ring` |

### A — async

The runtime’s own queue: Python `asyncio.Queue`, C# `Channel`, Rust
`tokio::sync::mpsc`.

JavaScript `p-queue` is a **concurrency limiter** (scheduler), not a
handoff queue. It is listed in the inventory; do not treat it as category A
for ranking.

## Not published yet

These are real categories. They get numbers only when a runner exists.
They never share a violin or rank table with T.

| ID | Category | Why it is different |
|----|----------|---------------------|
| **P** | Process / IPC | Serialization and OS pipes dominate |
| **S** | Shared memory | Same topology as P, different data path |
| **D** | Durable / local disk | fsync / WAL, not coordination primitives |
| **N** | Local broker | Client + localhost server — a **system** bench |

Brokers (Redis, Kafka, ZeroMQ) stay out of T/A charts.

## Not categories

These are **properties** that can apply inside T or A:

- bounded vs unbounded (backpressure)
- FIFO vs priority
- blocking vs spin vs yield
- SPSC vs MPMC (workload / pattern)

## Patterns

| Say | CSV `StringOrStream` | Work |
|-----|----------------------|------|
| SPSC | `bytes` | 1 producer, 1 consumer |
| MPMC | `stream` | 2 producers, 2 consumers |

“Stream” is a leftover column name. It is not I/O.
