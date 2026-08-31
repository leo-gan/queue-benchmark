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
| `StringOrStream` | `bytes` = **SPSC**, `stream` = **MPMC** (not a stream API) | grouping |
| `TestDataName` | Payload type id | grouping |

Column names are the shared ABI with serializer-benchmark. Docs always use
the queue words; the CSV keeps the original names so analysis and dashboard
code can be reused.
