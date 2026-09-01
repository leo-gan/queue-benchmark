# Metrics

Times are **nanoseconds**. Throughput is `1e9 / time_ns`.

| CSV column | Queue meaning | Rank |
|------------|---------------|------|
| `TimeEnq` | Enqueue (produce) | high |
| `TimeDeq` | Dequeue (consume) | high |
| `TimeHandoff` | Handoff / round-trip | high (primary rank) |
| `OpPerSecEnq` / `Deq` / `Handoff` | Derived ops/sec | high |
| `Size` | Payload bytes moved | high |
| `LibraryName` / `LibraryVersion` | Implementation + installed version | high |
| `FidelityScore` | 1.0 = every item arrived in order | high |
| `MemoryPeakBytes` | Peak allocation when the runner can measure it | medium |
| `CpuTimeNs` | Optional process CPU time for that repetition | high (derived) |
| `Pattern` | `bytes` = **SPSC**, `stream` = **MPMC** (not a stream API); also `1p4c` / `4p1c` / `4p4c` | grouping |
| `TestDataName` | Payload type id | grouping |

Derived first-class stats (not CSV columns):

| Stats field | Meaning | Rank |
|-------------|---------|------|
| `handoff_p999_ns` | 99.9th percentile of handoff ns | high |
| `msgs_per_cpu_sec` | `DataTypeInstanceCount / mean(CpuTimeNs)/1e9` | high |
| `library` / `library_version` | Implementation identity in stats JSON | grouping |

`msgs_per_cpu_sec` is null when `CpuTimeNs` is missing. Do not invent a
CPU-second number from wall time.

New writes use these names. The parser still accepts leftover
serializer-benchmark columns (`SerializerName`, `TimeSer`, `StringOrStream`,
…) so historical logs keep loading.
