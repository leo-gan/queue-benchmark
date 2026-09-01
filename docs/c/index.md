# C

| | |
|--|--|
| Runner | `c/` |
| Script | `./c/scripts/run-benchmarks.sh smoke` |
| Logs | `logs/c/` |
| Runtime | C11 + pthread, CMake |

| Log name | Category | Communication | Library | Notes |
|----------|----------|---------------|---------|-------|
| `mutex-queue` | locked | T (thread) | harness | pthread mutex + ring |
| `lfqueue` | concurrent | T (thread) | lfqueue (vendored) | Lock-free MPMC FIFO |
| `spsc-ring` | spsc | T (thread) | harness | Single-producer ring; MPMC skipped |
| `steal-deque` | work-stealing | T (thread) | harness | Owner-push / steal-from-top |
| `pipe-ipc` | concurrent | P (process) | harness | Opt-in pipe + fork |
| `shared-ring` | spsc | S (shared) | harness | Opt-in mmap + fork ring |
| `sqlite-queue` | durable | D (durable) | sqlite3 | Opt-in SQLite queue |

ZeroMQ, hiredis, and Concurrency Kit are **out of this lab**. See
[C library selection](library-selection.md).
