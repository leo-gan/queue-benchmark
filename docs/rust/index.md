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
