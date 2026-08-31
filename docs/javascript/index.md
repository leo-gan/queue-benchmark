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
| `p-queue` | async | — | p-queue | Concurrency limiter, not a handoff queue |
