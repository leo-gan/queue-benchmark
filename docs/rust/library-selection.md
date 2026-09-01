# Rust library selection

Same include/exclude rule as [Python](../python/library-selection.md): measure
**local handoff**. Brokers are category N. Job runners are not queues.

## Decision

| Decision | Crates |
|----------|--------|
| **Already in** | `std-mpsc`, `crossbeam-channel`, `crossbeam-queue`, `tokio-mpsc`, `steal-deque`, opt-in P/S/D |
| **Added** | `flume` (sync face), `async-channel` |
| **Out — overlapping T MPMC** | `kanal`, `thingbuf`, `loole` (same question as flume/crossbeam) |
| **Out — job / worker frameworks** | `apalis`, `faktory`, `sidekiq` rust ports |
| **Out — category N** | `lapin`, `rdkafka`, `redis`, `zeromq` |

`flume` and `kanal` were listed out of scope when the lab kept a minimum set.
`flume` is now in as the popular third-party MPMC (sync face only), the same
reason `janus` is in for Python A. `kanal` stays out so we do not add a third
T channel in one pass.

## In this lab

| Log name | Category | Why |
|----------|----------|-----|
| `std-mpsc` | T | Stdlib MPSC. Already present. |
| `crossbeam-channel` | T | Production MPMC. Already present. |
| `flume` | T | Popular MPMC, no `unsafe`. Sync face only — not mixed with async. **Added.** |
| `crossbeam-queue` | T | Lock-free `SegQueue`. Already present. |
| `tokio-mpsc` | A | Tokio unbounded MPSC. Already present. |
| `async-channel` | A | Runtime-agnostic async **MPMC**. Second A library, like Python `janus`. **Added.** |

The hybrid sync+async path on `flume` is not a category and is not timed.
