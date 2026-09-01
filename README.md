# Multi-Language Queue Benchmark

[![Site](https://img.shields.io/badge/site-documentation-indigo?style=flat-square)](https://leo-gan.github.io/queue-benchmark/)
[![Dashboard](https://img.shields.io/badge/dashboard%20%7C%20live-brightgreen?style=flat-square)](https://leo-gan.github.io/queue-benchmark/dashboard/)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE)
[![Languages](https://img.shields.io/badge/languages-5-informational?style=flat-square)](#supported-languages)

Compare in-process queue libraries across **Python, Rust, JavaScript, C#, and C**.

| Start here | |
|------------|--|
| **Home** | [Documentation](https://leo-gan.github.io/queue-benchmark/) |
| **Numbers** | [Live dashboard](https://leo-gan.github.io/queue-benchmark/dashboard/) |
| **Experiments** | [One-question tests](https://leo-gan.github.io/queue-benchmark/experiments/) |
| **Benchmarks** | [Design](https://leo-gan.github.io/queue-benchmark/analysis/BENCHMARK_DESIGN/) · [Methodology](https://leo-gan.github.io/queue-benchmark/analysis/ANALYSIS_METHODOLOGY/) · [Metrics](https://leo-gan.github.io/queue-benchmark/analysis/METRICS/) |

---

## Who it is for

| Audience | Use case |
|----------|----------|
| **Students** | Queue types, backpressure, what “fast” actually means |
| **System integrators** | Pick an in-process queue that fits the runtime |
| **Researchers** | Reproducible measurement and one-question experiments |
| **Library authors** | Add a queue, version A/B, regression checks |

---

## Supported languages

- [C](https://leo-gan.github.io/queue-benchmark/c/) — `mutex-queue`, `lfqueue`, `spsc-ring`
- [C# (.NET)](https://leo-gan.github.io/queue-benchmark/c-sharp/) — `Queue+lock`, `ConcurrentQueue`, `BlockingCollection`, `Channel`
- [JavaScript](https://leo-gan.github.io/queue-benchmark/javascript/) — `Array`, `denque`, `yocto-queue`, `fastq`, `p-queue` (scheduler)
- [Python](https://leo-gan.github.io/queue-benchmark/python/) — `deque-lock`, `queue.Queue`, `queue.SimpleQueue`, `asyncio.Queue`, `janus`, `spsc-ring`
- [Rust](https://leo-gan.github.io/queue-benchmark/rust/) — `std-mpsc`, `crossbeam-channel`, `flume`, `tokio-mpsc`, `async-channel`, `crossbeam-queue`

[Adding a language](https://leo-gan.github.io/queue-benchmark/analysis/ADDING_A_LANGUAGE/) · [Adding a queue](https://leo-gan.github.io/queue-benchmark/analysis/ADDING_A_QUEUE/).

This suite measures **local** queues on one machine. Compare inside one
language and one communication category: **thread**, **async**, and
opt-in **process / IPC**, **shared memory**, and **durable / disk**.
Network brokers (Redis, Kafka, ZeroMQ) need a different lab — never on
the same chart as `deque-lock`.

---

## Try it: benchmark Python queues in ~60 seconds

Requires a recent Python 3 and [uv](https://docs.astral.sh/uv/) (or pip). No Docker.

```bash
git clone https://github.com/leo-gan/queue-benchmark.git
cd queue-benchmark

./scripts/check-host-requirements.sh python   # optional: see what's missing
./scripts/install-host-requirements.sh python # optional: user-local toolchains

cd python && ./scripts/run-benchmarks.sh smoke
# → logs/python/YYYY-MM-DD-HHMMSS.csv
```

Then run `analyze-benchmarks -l python` after installing the analysis package.

Prefer Rust? `./scripts/run-all-benchmarks.sh --mode smoke --lang rust`

---

## Quick start

Benchmark runners run **natively on the host** (no Docker). Prepare toolchains once,
then run (project deps like `uv sync` / `npm install` still happen inside each runner).

```bash
# 1) Host toolchains (compilers/runtimes only)
./scripts/check-host-requirements.sh
./scripts/install-host-requirements.sh
./scripts/install-host-requirements.sh csharp   # one language

# 2) Smoke one language
./python/scripts/run-benchmarks.sh smoke
# or: ./rust/scripts/run-benchmarks.sh smoke

# Orchestrator: all languages or one language
./scripts/run-all-benchmarks.sh --mode all-single
./scripts/run-all-benchmarks.sh --mode full --lang rust

# Analysis package (writes reports/; Dashboard via sync-data.py)
cd analysis && uv pip install -e .   # or: pip install -e .
analyze-benchmarks
analyze-benchmarks -l python
analyze-benchmarks --compare-a rust:2026-08-31-120000 --compare-b rust:latest
```

**Modes**: `smoke` (2 reps) · `all-single` (10) · `full` (100) · `research` (500).

`analyze-benchmarks` writes `reports/`; Dashboard via `sync-data.py`. Review and
commit before `publish-docs` deploys the site.

---

## Test data

Shared **payload types**: `message`, `document`, `telemetry`, `strings`, and `event`.

Catalog and defaults: `schemas/data_catalog_v2.yaml`. Run matrices: `config/library/`.

---

## Statistics

- [Benchmark design](https://leo-gan.github.io/queue-benchmark/analysis/BENCHMARK_DESIGN/)
- [Analysis methodology](https://leo-gan.github.io/queue-benchmark/analysis/ANALYSIS_METHODOLOGY/)
- [Metrics catalog](https://leo-gan.github.io/queue-benchmark/analysis/METRICS/)

Compare queues **within one language and one category**. Cross-language
absolute times are directional only — runtimes and GCs differ.
[Comparison rules](https://leo-gan.github.io/queue-benchmark/analysis/COMPARISON_RULES/):
no global winner, no broker next to `deque-lock`.

---

## CSV contract

Every language writes the same columns (nanoseconds). Domain mapping:

| Column | Queue meaning |
|--------|---------------|
| `LibraryName` / `LibraryVersion` | Implementation + installed version |
| `TimeEnq` | Enqueue ns |
| `TimeDeq` | Dequeue ns |
| `TimeHandoff` | Handoff ns |
| `Pattern` | `bytes` = **SPSC**, `stream` = **MPMC** (not I/O) |
| `Size` | Payload bytes |

See [architecture](https://leo-gan.github.io/queue-benchmark/analysis/architecture/).

---

*Authored by Leonid Ganeline*
