# C library selection

Same include/exclude rule as [Python](../python/library-selection.md): measure
**local handoff**. Brokers are category N. Job runners are not queues.

C has almost no commonly packaged in-process FIFO on the host (no crates.io /
PyPI analog). `liblfds` and Concurrency Kit are real libraries but they are
system packages with a heavy build story. This pass vendors one small,
BSD-2-Clause lock-free MPMC instead of adding a new host requirement.

## Decision

| Decision | Libraries |
|----------|-----------|
| **Already in** | `mutex-queue`, `spsc-ring`, `steal-deque`, opt-in P/S/D |
| **Added** | `lfqueue` (vendored Taymindis/lfqueue) |
| **Out — host-heavy lock-free kits** | liblfds, Concurrency Kit (`ck_ring` / `ck_fifo`) |
| **Out — category N** | nanomsg / nng, ZeroMQ, hiredis, librdkafka |

## In this lab

| Log name | Category | Why |
|----------|----------|-----|
| `mutex-queue` | T / locked | pthread mutex + condvar ring. Already present. |
| `lfqueue` | T / concurrent | Vendored lock-free MPMC FIFO. The analog of Rust `crossbeam-queue`. **Added.** |
| `spsc-ring` | T / spsc | Harness ring. Already present. |

`lfqueue` has no condvar; wakeup cells are skipped (spin-only empty pop).
