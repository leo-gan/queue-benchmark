# Rust

| | |
|--|--|
| Runner | `rust/` |
| Script | `./rust/scripts/run-benchmarks.sh smoke` |
| Logs | `logs/rust/` |
| Runtime | rustc / cargo (stable) |

| Log name | Category | Crate | Notes |
|----------|----------|-------|-------|
| `std-mpsc` | concurrent | std | MPSC only; MPMC cells skipped |
| `crossbeam-channel` | concurrent | crossbeam-channel | Unbounded MPMC |
| `tokio-mpsc` | async | tokio | Unbounded async MPSC |
