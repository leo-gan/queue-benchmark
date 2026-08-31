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

Python opt-in runners exist. They never share a violin or rank table with T.
The dashboard Category filter includes Thread / Async / Process / Shared /
Durable / Other.

| ID | Category | Why it is different | First tests when a runner exists |
|----|----------|---------------------|----------------------------------|
| **P** | Process / IPC | Serialization and OS pipes dominate | 1P1C 64 B vs 64 KiB vs 1 MB; report MB/s and msgs/s separately |
| **S** | Shared memory | Same topology as P, different data path | 1P1C GB/s vs the P number on the same payload |
| **D** | Durable / local disk | fsync / WAL, not coordination primitives | Durability off vs fsync on; kill −9 recovery |
| **N** | Local broker | Client + localhost server — a **system** bench | Separate report, labeled “localhost” |

Brokers (Redis, Kafka, ZeroMQ) stay out of T/A charts.

The dashboard **Category** control filters the current language’s table
to Thread (T), Async (A), or Other (`p-queue` today). P/S/D have no
series yet.

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
