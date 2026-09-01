# Metrics

This lab ranks **in-process queues**, not encodings. Times are nanoseconds.
Throughput is derived: `1e9 / time_ns`. Payload **size** (256 B or 4 KiB) is the sample, not a library score.
Never call it a fixture.

## What we rank

| Field | Meaning | Why |
|-------|---------|-----|
| `TimeHandoff` / `handoff_median_ns` | Enqueue + dequeue wall time | Primary rank. Producer-only put/s can lie. |
| `TimeEnq` / `enq_median_ns` | Produce cost | Split of the handoff |
| `TimeDeq` / `deq_median_ns` | Consume cost | Split of the handoff |
| `avg_ops_per_sec` | `1e9 / mean(TimeHandoff)` | Same clock, easier to read |
| `handoff_p95_ns` / `p99` / `p999` | Tail of the same handoff series | A lock that is fast on the median and stalls on p99 is not “fast” |
| `msgs_per_cpu_sec` | `n / mean(CpuTimeNs)` | Spin can win latency and burn cores. Null if `CpuTimeNs` is missing. |

Do **not** invent `msgs_per_cpu_sec` from wall time.

## What we do not rank

| Field | Why it exists | What to do with it |
|-------|---------------|--------------------|
| `Size` / `SizeGzip` / `SizeZstd` / `median_size_bytes` | Serializer leftovers. Payload bytes are the **data type**, not a result. | **Removed.** New CSVs and stats do not write these. Old logs may still contain `Size`; analysis ignores it. |
| `mean_fidelity` | `FidelityScore` = fraction of items that arrived in order. | **Gate**, not a score. If `< 1`, the row is invalid for ranking. Typical value is `1.0`. |
| `mean_memory_peak_bytes` | Process RSS (`getrusage` / `PeakWorkingSet64` / `process.memoryUsage().rss`). | Provenance. Usually the process, not the queue. Do not run a “most compact” contest on it. |
| `StreamMode` / honesty | Serializer “native vs adapted stream I/O”. There is no stream I/O in this suite. `Pattern=stream` means **MPMC**. | Do not show an honesty column. |
| `OpPerSecEnq` / `Deq` / `Handoff` in the CSV | Convenience copies of `1e9 / Time*`. | Analysis recomputes from times. Do not treat CSV ops as a second clock. |

## Identity (not metrics)

`Language`, `LibraryName`, `LibraryVersion`, `Pattern`, `TestDataName`,
`DataTypeInstanceCount`, `TypeConfigHash`, `Repetitions`, `RepetitionIndex`,
`RunOrder`, `SchedulePosition`, `NativeKind` (implementation family label).

`Pattern`: `bytes` = SPSC, `stream` = MPMC 2P2C, plus named `1p4c` / `4p1c` /
`4p4c`.

## Derived stats (not CSV columns)

Percentiles, std, MAD, CV, bootstrap CI, Cliff’s δ vs the fastest peer — see
[ANALYSIS_METHODOLOGY](ANALYSIS_METHODOLOGY.md). `runs` / `outliers_removed`
are provenance.

## Missing on purpose

| Tempting metric | Why it is not a warehouse column |
|-----------------|----------------------------------|
| Empty-queue wakeup | Experiment 5. Needs a different loop than “enqueue all, dequeue all”. |
| Occupancy / depth | Not observed by the harness. |
| Fairness under steal | Experiment-level, not a single number. |
| Encoded size / gzip | Not a queue. |
| Cross-language rank | Different runtimes. Directional only. |

## CSV ABI

New writes keep the existing header so historical logs still parse. The
parser still accepts leftover serializer-benchmark names (`SerializerName`,
`TimeSer`, `StringOrStream`, …).

Meaning of the timed columns:

| CSV column | Queue meaning |
|------------|---------------|
| `TimeEnq` | Enqueue ns |
| `TimeDeq` | Dequeue ns |
| `TimeHandoff` | Handoff ns |
| `CpuTimeNs` | Optional process CPU time for that repetition |
| `FidelityScore` | 1.0 = every item arrived in order |
| `MemoryPeakBytes` | Peak RSS when the runner can measure it |
