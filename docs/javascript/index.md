# JavaScript

| | |
|--|--|
| Runner | `javascript/` |
| Script | `./javascript/scripts/run-benchmarks.sh smoke` |
| Logs | `logs/javascript/` |
| Runtime | Node.js 18+ |

| Log name | Category | Package | Notes |
|----------|----------|---------|-------|
| `Array` | locked | builtin | `push` / `shift` SPSC baseline |
| `fastq` | concurrent | fastq | In-process job queue |
| `p-queue` | async | p-queue | Promise concurrency queue |
