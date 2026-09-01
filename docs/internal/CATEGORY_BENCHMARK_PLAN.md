# Category and benchmark plan

Agreed design for queue categories and the single-machine benchmark
matrix. Source notes: `docs/temp/methodology.review.md`,
`docs/temp/methodology.review_2.md`.

**Do not compare libraries across communication categories.**
**Do not crown a global “fastest queue.”**
Experiments 1–12, Python P/S/D runners, P×C harness, work-stealing
family, and wakeup/burst/cancel in every language are in this pass.
See [IMPLEMENTATION_RUN.md](IMPLEMENTATION_RUN.md) for the 2026-08-31
gap-close. Category **N** stays unpublished.

## Rule

Compare **inside one language and one communication category**.
Implementation family (locked, concurrent, spsc-ring, …) is a *label*
inside a category, not a comparison boundary of its own.

CSV `Pattern` (formerly `StringOrStream`):

| Logged value | Queue meaning |
|--------------|---------------|
| `bytes` | SPSC (1 producer, 1 consumer) |
| `stream` | MPMC (today: 2 producers, 2 consumers) |

The dashboard and methodology must say **SPSC / MPMC**, never “stream API.”

## Communication categories

| ID | Category | What crosses the queue | Published now? |
|----|----------|------------------------|----------------|
| **T** | Thread / in-process | Same process, OS threads | Yes |
| **A** | Async / event-loop | Same process, tasks on a loop | Yes |
| **P** | Process / IPC | Processes via pipe/socket + serialize | Yes (Python opt-in; exp. 10) |
| **S** | Shared memory | Processes, bytes in a mapped region | Yes (Python opt-in; exp. 11) |
| **D** | Durable / local disk | Process + fsync / WAL / sqlite | Yes (Python opt-in; exp. 12) |
| **N** | Local broker | Client + localhost server | Later, separate **system** report |

Remote multi-node brokers stay out of this lab.

**Not categories** (apply inside T/A/P/S/D): bounded vs unbounded, FIFO vs
priority, blocking vs spin vs yield, SPSC / MPSC / SPMC / MPMC.

### T families (sub-labels only)

| Family | Role | Examples |
|--------|------|----------|
| locked | Mutex baseline | `deque-lock`, `Queue+lock`, `Array`, `mutex-queue` |
| concurrent | Thread-safe MPSC/MPMC | `queue.Queue`, `queue.SimpleQueue`, `ConcurrentQueue`, `crossbeam-channel`, `fastq` |
| spsc-ring | No mutex on the happy path | C `spsc-ring`, Python `spsc-ring` |
| work-stealing | Steal from the other end | Python `steal-deque`, Rust `crossbeam-deque`, C# / C / JS `steal-deque` |

Async channels (`asyncio.Queue`, `Channel`, `tokio::mpsc`) live in **A**.

## Tests

Always-on axes: language, category, family, pattern (`bytes` SPSC,
`stream` 2P2C, plus `1p4c` / `4p1c` / `4p4c` on the default matrix),
bound, payload, mode (smoke / all-single / full).

Primary metrics: completed handoffs/s, enqueue ns, dequeue ns, end-to-end
handoff, p50/p99/`total_p999_ns`, peak RSS, `msgs_per_cpu_sec` when
`CpuTimeNs` is present, fidelity (no loss, no dup; FIFO only if the API
promises it).

### T — thread / in-process

| ID | Question | Status |
|----|----------|--------|
| T1 | 1P1C, 64–256 B | Experiment 1 |
| T2 | Same, 256 B vs 4 KiB | Experiment 2 |
| T3 | 1P4C, 4P1C, 4P4C | Experiment 3 |
| T4 | Bounded + slow consumer | Experiment 4 |
| T5 | Empty-queue wakeup | Experiment 5 |
| T6 | Burst then idle | Experiment 6 |

### A — async

| ID | Question | Status |
|----|----------|--------|
| A1 | 1 task / 1 task, small payload | Covered by the default SPSC cell |
| A2 | Many waiting consumers | Experiment 7 |
| A3 | Bounded async backpressure | Experiment 8 |
| A4 | Timeout / cancel | Experiment 9 |

JS `p-queue` is a **concurrency limiter**, not a handoff queue. Reclassify
it (do not rank it against `asyncio.Queue`).

### P / S / D

Opt-in runners exist in every language (`pipe-ipc` / Python
`multiprocessing.Queue` for P, `shared-ring` for S, `sqlite-queue` for D).
Each has its own experiment folder (10–12) and dashboard filter. No
shared violin with T.

### Never

- One number for “the fastest queue”
- Cross-language rank
- Redis (or any broker) on the same plot as `deque-lock`

## Implementation order

- [x] **PR 1** — Plan + T/A as published categories + SPSC/MPMC labels +
  benchmark design docs. No `docs/theory/`, no `experiments/`.
  [#10](https://github.com/leo-gan/queue-benchmark/pull/10)
- [x] **PR 2** — Second SPSC ring (Python), lock-free MPMC (`crossbeam-queue`
  in Rust), reclassify `p-queue` as `scheduler`.
  [#11](https://github.com/leo-gan/queue-benchmark/pull/11)
- [x] **PR 3** — P/S/D scaffolding in analysis docs + dashboard category filter
  (T/A now; P/S/D when data exists). No runners, no experiments.
  [#12](https://github.com/leo-gan/queue-benchmark/pull/12)
- [x] **PR 4** — Comparison never-rules as a first-class analysis page.
  [#13](https://github.com/leo-gan/queue-benchmark/pull/13)

## PR Plan

### PR 1: Publish T/A categories and SPSC/MPMC labels

- **Description:** Store this plan. Rewrite analysis category/methodology
  docs so T and A are the published comparison boundaries. Relabel
  dashboard and docs: `bytes` → SPSC, `stream` → MPMC. Add
  `docs/analysis/BENCHMARK_DESIGN.md`. Do not touch `docs/theory/` or
  `experiments/`.
- **Files/components affected:** `docs/internal/CATEGORY_BENCHMARK_PLAN.md`,
  `docs/analysis/*`, `docs/internal/DESIGN.md`, `README.md`, `mkdocs.yml`,
  `config/benchmark_config.yaml`, `config/library/README.md`,
  `dashboard/index.html`, `dashboard/main.js`, `docs/{c,c-sharp,javascript,python,rust}/index.md`
- **Dependencies:** None

### PR 2: T/A library gaps

- **Description:** Add a Python SPSC ring (SPSC only). Add Rust
  `crossbeam-queue` as an explicit lock-free MPMC. Reclassify JavaScript
  `p-queue` as `scheduler` (still runnable so existing experiment YAML
  keeps working). Update language inventory pages. Do not edit
  `experiments/` or `docs/theory/`.
- **Files/components affected:** `python/src/benchmark/queues/`,
  `python/tests/`, `config/benchmark_config.yaml`, `rust/`,
  `javascript/src/runner.js`, `javascript/README.md`,
  `docs/python/index.md`, `docs/rust/index.md`, `docs/javascript/index.md`
- **Dependencies:** PR 1

### PR 3: P/S/D scaffolding and category filter

- **Description:** Document unpublished P/S/D/N categories and their
  tests. Add a dashboard category filter (Thread / Async / Other) driven
  by a catalog derived from config. No P/S/D runners. No experiments.
- **Files/components affected:** `docs/analysis/queue_categories.md`,
  `docs/analysis/BENCHMARK_DESIGN.md`, `dashboard/`,
  `config/benchmark_config.yaml`
- **Dependencies:** PR 2

### PR 4: Comparison never-rules

- **Description:** Add `docs/analysis/COMPARISON_RULES.md` and point
  README, claims, and the dashboard orientation at it.
- **Files/components affected:** `docs/analysis/COMPARISON_RULES.md`,
  `docs/analysis/index.md`, `docs/analysis/CLAIMS_AND_REPLICATION.md`,
  `README.md`, `mkdocs.yml`, `dashboard/index.html`
- **Dependencies:** PR 3
