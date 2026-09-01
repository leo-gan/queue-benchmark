# queue-benchmark design

Refactor of `GLD.QueueBenchmark` onto the **serializer-benchmark measurement OS**:
config → native runners → shared CSV → analysis → dashboard → experiments → CI/docs/skills.

This document is the source of truth for the stacked PRs. Domain words change
(serializer → queue library). Folder contracts, modes, and the CSV ABI stay.

## Goals

- Project and folder name: **queue-benchmark**.
- Same repo design as serializer-benchmark: docs, scripts, languages, dashboard,
  experiments, CI/CD, skills.
- Only a **necessary minimum** of queue libraries, covering the main types.
- Five languages already in this repo: Python, Rust, JavaScript, C#, C.

## Key decisions

1. **Keep the CSV ABI (output schema 1.1).** Analysis and dashboard already speak
   `SerializerName`, `TimeSer`, `TimeDeser`, `StringOrStream`. Mapping:

   | CSV column | Queue meaning |
   |------------|---------------|
   | `SerializerName` / `SerializerVersion` | Queue library name / version |
   | `TimeSer` | Enqueue (produce) ns |
   | `TimeDeser` | Dequeue (consume) ns |
   | `TimeSerAndDeser` | Handoff / round-trip ns |
   | `Size` | Payload bytes moved in that repetition |
   | `StringOrStream` | Pattern: **SPSC** (logged as `bytes`) or **MPMC** (logged as `stream`) |
   | `TestDataName` | Payload type id (`message`, `document`, …) |
   | `FidelityScore` | 1.0 if every item arrived in order; else < 1 |

   Keeping names lets us reuse the analysis package and dashboard pipeline
   unchanged. Docs explain the mapping.

2. **Five languages, not twelve.** The original project already had C, C#, JS,
   Python, Rust. Adding seven stub languages would be fake coverage.

3. **Minimum libraries covering main queue types**

   Communication categories **T** (thread) and **A** (async) are the
   comparison boundary. Families inside T: locked, concurrent, spsc-ring,
   work-stealing.

   | Type | Meaning | Implementations |
   |------|---------|-----------------|
   | locked | Mutex + stdlib queue (baseline) | Python `deque-lock`, C# `Queue+lock`, JS `Array`, C `mutex-queue` |
   | concurrent | Thread-safe MPMC / MPSC | Python `queue.Queue` + `queue.SimpleQueue`, C# `ConcurrentQueue`, Rust `std-mpsc` + `crossbeam-channel` + `crossbeam-queue`, JS `fastq` |
   | async | Event-loop / async channel (category A) | Python `asyncio.Queue` + `janus` (async face), C# `Channel`, Rust `tokio::sync::mpsc` |
   | spsc-ring | Single-producer ring | C `spsc-ring`, Python `spsc-ring` |
   | work-stealing | Owner-push / steal-from-top | Python `steal-deque`, Rust `crossbeam-deque`, C# / C / JS `steal-deque` |
   | scheduler | Not a handoff queue | JS `p-queue` (concurrency limiter) |

   Category plan: [CATEGORY_BENCHMARK_PLAN.md](CATEGORY_BENCHMARK_PLAN.md).
   Out of scope for T/A charts: Redis, ZeroMQ, Celery, BullMQ, flume,
   kanal, BufferBlock, rxjs. `janus` is in as category A (async face
   only); the hybrid thread↔async path is not a category.

4. **Same modes.** smoke=2, all-single=10, full=100, research=500.

5. **Same payload catalog type ids** (`message`, `document`, `telemetry`,
   `strings`, `event`) so the run-config expander and analysis tests stay
   compatible. Runners treat them as payload-size / shape knobs, not object
   graphs to serialize.

6. **Native host runners.** No Docker. `scripts/run-benchmarks.sh` per language.

7. **Slim theory.** Queues 101/201/301 only — do not copy the serializer 401 labs.

## Repository layout

```
queue-benchmark/
  README.md LICENSE pyproject.toml mkdocs.yml
  config/benchmark_config.yaml
  config/library/{smoke,default}.yaml
  schemas/data_catalog_v2.yaml
  scripts/{lib/config.sh,read-config.py,run-all-benchmarks.sh,
           check-host-requirements.sh,install-host-requirements.sh,
           resolve_run_config.py,verify-results.sh}
  analysis/                          # reused measurement package
  python/ rust/ javascript/ c-sharp/ c/
  dashboard/
  experiments/{lib,01-spsc-handoff,02-payload-size}
  docs/  .github/workflows/  .grok/skills/
```

## Measurement model

1. **Prepare (untimed):** allocate payload bytes, construct the queue, spawn
   workers if needed. Do not move items here.
2. **Timed loop:** enqueue all items, dequeue all items. Write every repetition
   including warmup index 0.
3. **Analysis** drops warmup, applies IQR, bootstrap CIs, ranks by
   `total_median_ns` (handoff).

Compare queues **within one language**. Cross-language times are directional only.

## PR plan

See the bottom of this file.

## Open questions

None. Judgement calls above are final for this refactor.

---

## PR Plan

### PR 1: Scaffold the measurement OS

- **Title:** Scaffold queue-benchmark on the serializer-benchmark repo design
- **Files/components affected:** README, LICENSE, pyproject.toml, .gitignore,
  config/, schemas/, scripts/, analysis/, docs skeleton, mkdocs.yml,
  docs/internal/DESIGN.md
- **Dependencies:** None
- **Description:** Rename the project, delete the old ad-hoc runners, install
  the shared config/scripts/analysis contract. No language runners yet.

### PR 2: Five language harnesses

- **Title:** Add Python, Rust, JavaScript, C#, and C queue runners
- **Files/components affected:** python/, rust/, javascript/, c-sharp/, c/,
  docs/{python,rust,javascript,c-sharp,c}/index.md
- **Dependencies:** PR 1
- **Description:** Each language implements `scripts/run-benchmarks.sh` and
  writes the shared CSV. Only the minimum libraries in the table above.

### PR 3: Dashboard and experiments

- **Title:** Add dashboard and first queue experiments
- **Files/components affected:** dashboard/, experiments/, docs/experiments/
- **Dependencies:** PR 2
- **Description:** Vite dashboard (5 languages) + two one-question experiments
  (SPSC handoff bakeoff, payload-size ranking).

### PR 4: Docs, skills, and CI/CD

- **Title:** Add docs site, agent skills, and CI/CD
- **Files/components affected:** docs/ (theory + analysis), .grok/skills/,
  .github/workflows/, mkdocs.yml
- **Dependencies:** PR 3
- **Description:** Material site tabs, adapted skills (prepare-pr, clean-logs,
  implement-experiment, review-suspicious-results, improve-docs), smoke CI
  and docs publish.
