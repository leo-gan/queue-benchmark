# JavaScript

| | |
|--|--|
| Runner | `javascript/` |
| Script | `./javascript/scripts/run-benchmarks.sh smoke` |
| Logs | `logs/javascript/` |
| Runtime | Node.js 18+ |

| Log name | Category | Communication | Package | Notes |
|----------|----------|---------------|---------|-------|
| `Array` | locked | T (thread) | builtin | `push` / `shift` SPSC baseline |
| `denque` | locked | T (thread) | denque | O(1) circular deque; SPSC only |
| `yocto-queue` | locked | T (thread) | yocto-queue | O(1) linked-list FIFO; SPSC only |
| `fastq` | concurrent | T (thread) | fastq | In-process job queue |
| `p-queue` | scheduler | — | p-queue | Concurrency limiter, not a handoff queue |
| `steal-deque` | work-stealing | T (thread) | harness | Owner-push / steal-from-top |
| `pipe-ipc` | concurrent | P (process) | harness | Opt-in child-process pipe |
| `shared-ring` | spsc | S (shared) | harness | Opt-in SharedArrayBuffer worker ring |
| `sqlite-queue` | durable | D (durable) | node:sqlite | Opt-in SQLite queue |

BullMQ, Redis, and other broker/job libraries are **out of this lab**. See
[JavaScript library selection](library-selection.md).
