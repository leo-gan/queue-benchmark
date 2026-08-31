# Benchmark architecture

This page describes **how the suite is built**: folder layout, who the
measurements are for, what is timed, and where configuration lives.

| If you need… | Go here |
|--------------|---------|
| Statistics (warmup, outliers, confidence intervals) | [Analysis methodology](ANALYSIS_METHODOLOGY.md) |
| Payload shapes and size knobs | [Test data](test_data_configuration.md) |
| locked vs concurrent vs async | [Queue categories](queue_categories.md) |
| How to add another language | [Adding a language](ADDING_A_LANGUAGE.md) |
| How to add one library | [Adding a queue](ADDING_A_QUEUE.md) |

---

## One pipeline, four kinds of reader

Everyone uses the **same measurement contract** and the **same analysis path**.

| Reader | Primary question |
|--------|------------------|
| **Student or researcher** | Are the rankings inside one language trustworthy? |
| **Library author** | Can I drop in my queue? Did it get better or worse? |
| **System builder** | What fits *our* payload sizes and runtime? |
| **Maintainer** | Can I add a language without rewriting analysis? |

---

## Repository layout

| Path | Role |
|------|------|
| `config/benchmark_config.yaml` | Run modes, statistics defaults, language list, CSV schema |
| `schemas/` | Shared payload catalog |
| `logs/<language>/` | Timestamped result CSVs (gitignored) |
| `analysis/` | Python package that implements `analyze-benchmarks` |
| `python/`, `c-sharp/`, `rust/`, `c/`, `javascript/` | One benchmark runner per language |
| `docs/` | MkDocs site |
| `scripts/run-all-benchmarks.sh` | Orchestrates multi-language runs |

---

## What we measure {#measurement-model}

A fair timing experiment separates **preparation** (once, untimed) from **the loop**
(many times, timed).

1. **Prepare (not timed)**  
   Allocate payload bytes, construct the queue, spawn workers. **Do not move items
   here.** See [Timing honesty](TIMING_HONESTY.md).

2. **Timed loop** (for each repetition `i`):
   - enqueue every item → record **enqueue time** (`TimeSer`)
   - dequeue every item → record **dequeue time** (`TimeDeser`)
   - wall-clock of the pair → **handoff** (`TimeSerAndDeser`)
   - Check **fidelity** (every item arrived, in order). Failures go to an errors
     file; a broken handoff is never a speed win.

3. **Warmup**  
   Index `0` is written to the CSV. Analysis **drops** it from averages.

## CSV ABI

Column names match the serializer-benchmark contract so analysis and dashboard
code can be reused. Mapping:

| Column | Queue meaning |
|--------|---------------|
| `SerializerName` | Queue library name |
| `TimeSer` | Enqueue ns |
| `TimeDeser` | Dequeue ns |
| `TimeSerAndDeser` | Handoff ns |
| `StringOrStream` | `bytes` = SPSC, `stream` = MPMC |
| `Size` | Payload bytes |

## Patterns

- **SPSC** (`bytes`): one producer, one consumer. Every library must implement this.
- **MPMC** (`stream`): two producers, two consumers. Libraries that cannot do MPMC
  skip the cell rather than fake it.
