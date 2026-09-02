# 13 — Payload size sweep

**Question:** which payload sizes change the 1P1C ranking, and which are
redundant?

Every runner already builds an opaque byte string of a chosen length.
This folder asked which lengths change ranking, and which are just more
of the same.

Sizes in this run: **1 B, 64 B, 256 B, 4 KiB, 64 KiB**. One hundred items
per repetition. 1P1C only. One hundred repetitions (`full`).

```bash
./experiments/13-payload-size-sweep/run.sh python
./experiments/13-payload-size-sweep/run.sh
```

Do not compare times across languages. Read the rank tables in
`results.md`.
