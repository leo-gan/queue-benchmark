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
| `spsc-ring` | spsc | T (thread) | harness | Single-producer ring; MPMC skipped |
