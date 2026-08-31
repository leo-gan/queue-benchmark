# Queue categories

This suite covers the **main in-process types**. Brokers are out of scope.

| Category | What it is | Example |
|----------|------------|---------|
| **locked** | Mutex around a stdlib queue. Baseline. | Python `deque-lock`, C# `Queue+lock`, JS `Array`, C `mutex-queue` |
| **concurrent** | Thread-safe MPSC/MPMC. | Python `queue.Queue`, C# `ConcurrentQueue`, Rust `crossbeam-channel`, JS `fastq` |
| **async** | Event-loop / async channel. | Python `asyncio.Queue`, C# `Channel`, Rust `tokio::sync::mpsc`, JS `p-queue` |
| **spsc** | Single-producer ring (no mutex on the happy path). | C `spsc-ring` |

Compare libraries **inside one category** first. A locked deque and an async
channel answer different questions.
