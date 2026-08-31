---
hide:
  - title
---

# Multi-Language Queue Benchmark

Fair, reproducible measurements of **in-process queue libraries** across five languages.

This is a **measurement lab**, not a leaderboard of “the fastest queue in the world.”
Compare queues **inside one language and one category** (thread vs async).
Cross-language times are directional only.

| Go here | Why |
|---------|-----|
| [Benchmark design](analysis/BENCHMARK_DESIGN.md) | Categories, tests, how to read a result |
| [Comparison rules](analysis/COMPARISON_RULES.md) | What we never rank together |
| [Queue categories](analysis/queue_categories.md) | T (thread) and A (async) |
| [Architecture](analysis/architecture.md) | How the suite is built |
| [Modes](analysis/modes.md) | smoke / all-single / full / research |
| [Metrics](analysis/METRICS.md) | What the columns mean (enqueue / dequeue / handoff) |
| [Adding a queue](analysis/ADDING_A_QUEUE.md) | Drop in one library |
| [Adding a language](analysis/ADDING_A_LANGUAGE.md) | New runner contract |
| [Queues 101](theory/101/index.md) | Types, backpressure, lock vs lock-free |

## Languages

- [C](c/index.md)
- [C#](c-sharp/index.md)
- [JavaScript](javascript/index.md)
- [Python](python/index.md)
- [Rust](rust/index.md)

## Quick start

```bash
./scripts/check-host-requirements.sh python
./python/scripts/run-benchmarks.sh smoke
```
