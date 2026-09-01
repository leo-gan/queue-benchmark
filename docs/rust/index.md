# Rust

| | |
|--|--|
| Runner | `rust/` |
| Script | `./rust/scripts/run-benchmarks.sh smoke` |
| Logs | `logs/rust/` |
| Runtime | rustc / cargo (stable) |

| Log name | Category | Communication | Crate | Notes |
|----------|----------|---------------|-------|-------|
| `std-mpsc` | concurrent | T (thread) | std | MPSC only; MPMC cells skipped |
| `crossbeam-channel` | concurrent | T (thread) | crossbeam-channel | Unbounded MPMC |
| `tokio-mpsc` | async | A (async) | tokio | Unbounded async MPSC |
| `crossbeam-queue` | concurrent | T (thread) | crossbeam-queue | Lock-free `SegQueue` MPMC |
| `steal-deque` | work-stealing | T (thread) | crossbeam-deque | Chase-Lev injector / steal |
| `pipe-ipc` | concurrent | P (process) | std | Opt-in child-process pipe |
| `shared-ring` | spsc | S (shared) | memmap2 | Opt-in mmap ring |
| `sqlite-queue` | durable | D (durable) | rusqlite | Opt-in SQLite queue |
