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
| `ConcurrentQueue` | concurrent | T (thread) | stdlib | MPMC, non-blocking take |
| `BlockingCollection` | concurrent | T (thread) | stdlib | Blocking MPMC (`Add`/`Take`) |
| `Channel` | async | A (async) | stdlib | Unbounded `Channel<T>` |
| `steal-deque` | work-stealing | T (thread) | harness | Owner-push / steal-from-top |
| `pipe-ipc` | concurrent | P (process) | harness | Opt-in child-process pipe |
| `shared-ring` | spsc | S (shared) | harness | Opt-in memory-mapped ring |
| `sqlite-queue` | durable | D (durable) | Microsoft.Data.Sqlite | Opt-in SQLite queue |

Hangfire, RabbitMQ.Client, and `BufferBlock` are **out of this lab**. See
[C# library selection](library-selection.md).
