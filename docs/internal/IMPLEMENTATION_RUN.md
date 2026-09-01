# Implementation run: remaining original-spec gaps

Date: 2026-08-31  
Branch: `feat/complete-original-spec`  
Base: `773bea8` (`Implement remaining category-plan harness, experiments, and P/S/D runners (#17)`)

This note is the record of **this** implementation run. It is not a
methodology rewrite. After #17 the category plan was mostly landed, but
several original-spec items were still missing. This run implements those
items. Category **N** (localhost broker) stays out of this lab, as designed.

## What was still missing after #17

| Gap | After #17 | This run |
|-----|-----------|----------|
| True two-process **P** | Same-process `multiprocessing.Queue` pickle | Parent + child `Process` producers/consumers (`run_cross_process`) |
| True two-process **S** | Same-process mapped `Array` | Parent maps `Array`/`Value`; child process produce + consume |
| Work-stealing family | None | Python `steal-deque` (owner-push / steal-from-top) |
| Default matrix P×C | SPSC + 2P2C only | `bytes`, `stream`, `1p4c`, `4p1c`, `4p4c` |
| Wakeup / burst / cancel | Python only | Python, Rust, C#, C, JavaScript |
| p99.9 | Described, not first-class | `report_percentiles` includes 99.9 → `total_p999_ns` (label is `p999`, not `int(99.9)=99`) |
| Messages / CPU-second | Described, not first-class | Optional CSV `CpuTimeNs`; stats `msgs_per_cpu_sec` (high importance) |

**Still out of scope (by design):** category **N** (Redis / Kafka / localhost
broker). That is a system bench, not a data-structure bench.

## What this run ships

### 1. True two-process P and S (Python)

- `python/src/benchmark/queues/process_queue.py`
  - `run_cross_process(items, producers, consumers, capacity)` starts real
    `multiprocessing.Process` producers (`Queue.put`) and consumers
    (`Queue.get`), joins them, and times the wall handoff.
  - Adapter flag `cross_process = True`. Still `opt_in` (not in the default
    library matrix).
- `python/src/benchmark/queues/shared_ring.py`
  - Parent creates unlocked `Array`/`Value` ring; one child produces, one
    child consumes. SPSC only (`producers != 1 or consumers != 1` → skip).
- `python/src/benchmark/runner.py` dispatches `cross_process` adapters to
  those runners instead of in-process `_run_sync`.
- `freeze_support()` in `runner.main()` so spawn start methods do not
  re-enter the harness.

### 2. Work-stealing family

- New adapter `python/src/benchmark/queues/steal_deque.py` (`steal-deque`).
- Family label `work-stealing`. Communication **T**.
- Owner push = `deque.append` (bottom). Steal = `popleft` (top). The
  steal-from-top order is FIFO, so 1P1C fidelity stays 1.0.
- Registered in `ALL_QUEUES` and `config/benchmark_config.yaml`.
- This is a locked Chase-Lev *shape*, not a published lock-free steal
  algorithm. It exists so the family has a first member.

### 3. Default full matrix includes 1P4C / 4P1C / 4P4C

`config/library/default.yaml`:

```yaml
io_modes: [bytes, stream, 1p4c, 4p1c, 4p4c]
```

CSV `Pattern` values stay `bytes` = SPSC, `stream` = 2P2C.
Named patterns are first-class cells. Libraries that cannot do MPMC skip
those cells (existing `_can_run` / SPSC-only rules). A full bench is
about 2.5× the old SPSC+2P2C matrix.

### 4. Wakeup / burst / cancel in every language

`BENCHMARK_SPECIAL=wakeup|burst|cancel` (plus `BENCHMARK_WAIT_NS` for
wakeup). Experiments 05 / 06 / 09 already export these.

| Language | Wakeup | Burst | Cancel |
|----------|--------|-------|--------|
| Python | Blocking dequeue, parked thread | Sequential fill then drain | `asyncio.Queue` task cancel only |
| Rust | `crossbeam` bounded(1) + parked recv | Per-queue fill/drain | `tokio-mpsc` abort only |
| C# | `BlockingCollection` Take + parked task | Per-queue fill/drain | `Channel.ReadAsync` + `CancellationToken` only |
| C | `mutex-queue` condvar + parked thread | Fill/drain for both queues | **Skip** (no async queue) |
| JavaScript | Event-loop poll of a parked consumer | Per-queue fill/drain | `p-queue.clear()` of pending add()s only |

Skip rules (do not write a `(0,0)` row):

- Cancel is skipped unless the library is the language’s async/cancelable
  queue (`asyncio.Queue`, `tokio-mpsc`, `Channel`, JS `p-queue`).
- C has no async queue → experiment 09 writes no C rows.
- SPSC rings skip wakeup (they spin; that is not an OS wait).

### 5. First-class p99.9 and messages / CPU-second

- `statistics.report_percentiles` includes `99.9`.
- Percentile key: `str(p).replace(".", "")` when `p` is not an integer, so
  99.9 becomes `total_p999_ns` (not `total_p99_ns`).
- Metrics catalog: `total_p999_ns` and `msgs_per_cpu_sec` are **high**.
- Optional CSV column `CpuTimeNs` (parser + `BenchmarkLog`).
- `msgs_per_cpu_sec = instance_count / mean(CpuTimeNs)/1e9` when the
  column is present and positive.
- Emitted today: Python (`process_time_ns`), C (`CLOCK_PROCESS_CPUTIME_ID`),
  C# (`Process.TotalProcessorTime`), JavaScript (`process.cpuUsage`).
- Rust does not emit `CpuTimeNs` in this run (no extra crate). Analysis
  leaves `msgs_per_cpu_sec` null for those groups.

## Files touched

Harness / analysis

- `python/src/benchmark/queues/process_queue.py`
- `python/src/benchmark/queues/shared_ring.py`
- `python/src/benchmark/queues/steal_deque.py` (new)
- `python/src/benchmark/queues/__init__.py`
- `python/src/benchmark/runner.py`
- `python/src/benchmark/report.py`
- `python/tests/test_runner.py`
- `rust/src/main.rs`, `rust/Cargo.toml` (`tokio` `time` feature)
- `c-sharp/src/Program.cs`
- `c/src/main.c`
- `javascript/src/runner.js`, `javascript/test/runner.test.js`
- `analysis/src/benchmark_analysis/{stats,parser,metrics_catalog}.py`
- `analysis/tests/test_stats.py`
- `config/benchmark_config.yaml`
- `config/library/default.yaml`

Docs

- this file
- `docs/internal/CATEGORY_BENCHMARK_PLAN.md`
- `docs/internal/DESIGN.md`
- `docs/analysis/BENCHMARK_DESIGN.md`
- `docs/analysis/METRICS.md`
- `docs/analysis/queue_categories.md`
- `docs/python/index.md`

## How to verify

```bash
# Unit tests
(cd python && uv run pytest tests/test_runner.py -q)
(cd analysis && uv run pytest tests/test_stats.py -q)
(cd javascript && npm test)
dotnet build c-sharp/src/QueueBenchmark.csproj -c Release
cmake --build c/build

# Specials (need BENCHMARK_CELLS_TSV from a resolved run config)
export BENCHMARK_SPECIAL=wakeup BENCHMARK_WAIT_NS=1000000
# then the language runner all-single
```

Cross-process tests start real child processes (four items / three items).
They must pass on Linux fork.

## Follow-up run (all languages)

Landed on `feat/follow-ups-all-langs` after #18.

| Item | Status |
|------|--------|
| Category **N** | Still out of this lab |
| Work-stealing in every language | Rust `crossbeam-deque` Chase-Lev injector; C# / C / JS / Python `steal-deque` |
| P/S/D in C#, Rust, C, JS | `pipe-ipc`, `shared-ring`, `sqlite-queue` (opt-in, same names as experiments 10–12) |
| Rust `CpuTimeNs` | `CLOCK_PROCESS_CPUTIME_ID` via `libc` |
| Peak RSS | `MemoryPeakBytes` from `getrusage` / `PeakWorkingSet64` / `process.memoryUsage().rss` |
| Experiments 05 / 06 / 09 / 10 / 11 / 12 | Enabled for every language that has the adapter |

JS `shared-ring` is a `worker_threads` + `SharedArrayBuffer` ring (Node has no anonymous process mmap). C `pipe-ipc` / `shared-ring` use `fork`. C# / Rust / JS spawn the same binary as a child.
