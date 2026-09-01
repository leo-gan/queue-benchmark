# Rust Queue Benchmark

`std::sync::mpsc` (MPSC), `crossbeam-channel` / `flume` (MPMC),
`tokio::sync::mpsc` and `async-channel` (async).

```bash
cd rust
./scripts/run-benchmarks.sh smoke
```
