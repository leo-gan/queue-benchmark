# C

| | |
|--|--|
| Runner | `c/` |
| Script | `./c/scripts/run-benchmarks.sh smoke` |
| Logs | `logs/c/` |
| Runtime | C11 + pthread, CMake |

| Log name | Category | Library | Notes |
|----------|----------|---------|-------|
| `mutex-queue` | locked | harness | pthread mutex + ring |
| `spsc-ring` | spsc | harness | Single-producer ring; MPMC skipped |
