# 13 — Payload size sweep

**Question:** which payload sizes change the SPSC ranking, and which are
redundant?

This is not another named data type. Every runner already builds an opaque
byte string. The five catalog names (`message`, `event`, `telemetry`,
`strings`, `document`) are five lengths between 256 B and 4 KiB. This
folder asks whether the published suite needs those names at all, or only
one or two lengths.

Sizes in this run: **1 B, 64 B, 256 B, 4 KiB, 64 KiB**. One hundred items
per repetition. SPSC only. One hundred repetitions (`full`).

```bash
./experiments/13-payload-size-sweep/run.sh python
./experiments/13-payload-size-sweep/run.sh
```

Do not compare times across languages. Read the rank tables in
`results.md`.
