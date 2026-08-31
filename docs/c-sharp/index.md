# C#

| | |
|--|--|
| Runner | `c-sharp/` |
| Script | `./c-sharp/scripts/run-benchmarks.sh smoke` |
| Logs | `logs/csharp/` |
| Runtime | .NET 8 |

| Log name | Category | Communication | Package | Notes |
|----------|----------|---------------|---------|-------|
| `Queue+lock` | locked | T (thread) | stdlib | `Queue<T>` + `lock` |
| `ConcurrentQueue` | concurrent | T (thread) | stdlib | MPMC |
| `Channel` | async | A (async) | stdlib | Unbounded `Channel<T>` |
