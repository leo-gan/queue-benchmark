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
| `fastq` | concurrent | T (thread) | fastq | In-process job queue |
| `p-queue` | scheduler | — | p-queue | Concurrency limiter, not a handoff queue |
| `steal-deque` | work-stealing | T (thread) | harness | Owner-push / steal-from-top |
| `pipe-ipc` | concurrent | P (process) | harness | Opt-in child-process pipe |
| `shared-ring` | spsc | S (shared) | harness | Opt-in SharedArrayBuffer worker ring |
| `sqlite-queue` | durable | D (durable) | node:sqlite | Opt-in SQLite queue |
