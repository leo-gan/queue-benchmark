# Metrics

Times are **nanoseconds**. Throughput is `1e9 / time_ns`.

| CSV column | Queue meaning | Rank |
|------------|---------------|------|
| `TimeSer` | Enqueue (produce) | high |
| `TimeDeser` | Dequeue (consume) | high |
| `TimeSerAndDeser` | Handoff / round-trip | high (primary rank) |
| `OpPerSecSer` / `Deser` / `SerAndDeser` | Derived ops/sec | high |
| `Size` | Payload bytes moved | high |
| `SerializerName` / `SerializerVersion` | Queue library + installed version | high |
| `FidelityScore` | 1.0 = every item arrived in order | high |
| `MemoryPeakBytes` | Peak allocation when the runner can measure it | medium |
| `CpuTimeNs` | Optional process CPU time for that repetition | high (derived) |
| `StringOrStream` | `bytes` = **SPSC**, `stream` = **MPMC** (not a stream API); also `1p4c` / `4p1c` / `4p4c` | grouping |
| `TestDataName` | Payload type id | grouping |

Derived first-class stats (not CSV columns):

| Stats field | Meaning | Rank |
|-------------|---------|------|
| `total_p999_ns` | 99.9th percentile of handoff ns | high |
| `msgs_per_cpu_sec` | `DataTypeInstanceCount / mean(CpuTimeNs)/1e9` | high |

`msgs_per_cpu_sec` is null when `CpuTimeNs` is missing (Rust in this
pass). Do not invent a CPU-second number from wall time.

Column names are the shared ABI with serializer-benchmark. Docs always use
the queue words; the CSV keeps the original names so analysis and dashboard
code can be reused.
