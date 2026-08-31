# C#

| | |
|--|--|
| Runner | `c-sharp/` |
| Script | `./c-sharp/scripts/run-benchmarks.sh smoke` |
| Logs | `logs/csharp/` |
| Runtime | .NET 8 |

| Log name | Category | Package | Notes |
|----------|----------|---------|-------|
| `Queue+lock` | locked | stdlib | `Queue<T>` + `lock` |
| `ConcurrentQueue` | concurrent | stdlib | MPMC |
| `Channel` | async | stdlib | Unbounded `Channel<T>` |
