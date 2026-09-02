# 13-payload-size-sweep

Times are not comparable across languages.

Question: which 1P1C payload sizes change the ranking?

## Recommendation

Keep 256 B as the default small cell. Add one larger cell only when some language becomes copy-bound (handoff at least 2× and the pack collapses to about 1.3×) or the ranking inverts. Mid-pack swaps with a flat time scale are not a new size. A later inversion after the first copy-cost knee stays a research / experiment cell, not a third default type.

Do not confuse **payload bytes per item** with **how many items** move in one repetition (`data_type_instance_count`). This folder sweeps bytes per item at n = 100. n = 1 is the wakeup experiment. n = 1000 is a throughput / amortization check, not a third size.

**Published default matrix (two sizes)**

- `size_256` (256 B): baseline (pointer-bound / typical small message)
- `size_4096` (4 KiB): rust: copy-bound pack collapse (time ×9.24, spread 1.19×)

**Research / experiment only (not a default type)**

- `size_65536` (64 KiB): rust: rank inversion (Spearman -0.357); rust: first place crossbeam-queue -> std-mpsc and time ×282.37

**Redundant in this run**

- `size_1` (1 B): same first place as 256 B, no copy-bound pack collapse, no inversion.
- `size_64` (64 B): same first place as 256 B, no copy-bound pack collapse, no inversion.

## What this means for the published matrix

Every runner builds an opaque byte string. This sweep asked which lengths change 1P1C ranking. Python and C never change first place. JavaScript and C# only shuffle a close pair. Rust first changes at 4 KiB, when the queue copies every byte. Keep 256 B and 4 KiB on the default matrix. 1 B and 64 B match 256 B. 64 KiB is a later research cell, not a third published size.

## Per language vs 256 B

### python

| Size | First | Spearman | Flips | Time × | Spread |
|------|-------|---------:|------:|-------:|-------:|
| 1 B | queue.SimpleQueue | 1.000 | 0 | 0.94 | 16.54× |
| 64 B | queue.SimpleQueue | 0.964 | 1 | 0.98 | 15.92× |
| 256 B | queue.SimpleQueue | 1.000 | 0 | 1.00 | 16.35× |
| 4 KiB | queue.SimpleQueue | 1.000 | 0 | 1.07 | 16.28× |
| 64 KiB | queue.SimpleQueue | 1.000 | 0 | 1.17 | 16.46× |

See `python/results.md`.

### rust

| Size | First | Spearman | Flips | Time × | Spread |
|------|-------|---------:|------:|-------:|-------:|
| 1 B | crossbeam-queue | 0.786 | 3 | 0.99 | 2.55× |
| 64 B | crossbeam-queue | 0.964 | 1 | 0.84 | 2.40× |
| 256 B | crossbeam-queue | 1.000 | 0 | 1.00 | 2.14× |
| 4 KiB | flume | 0.750 | 4 | 9.24 | 1.19× |
| 64 KiB | std-mpsc | -0.357 | 13 | 282.37 | 1.35× |

See `rust/results.md`.

### javascript

| Size | First | Spearman | Flips | Time × | Spread |
|------|-------|---------:|------:|-------:|-------:|
| 1 B | fastq | 0.829 | 2 | 2.14 | 41.17× |
| 64 B | fastq | 0.829 | 2 | 0.99 | 44.91× |
| 256 B | fastq | 1.000 | 0 | 1.00 | 32.15× |
| 4 KiB | fastq | 0.899 | 1 | 1.03 | 36.32× |
| 64 KiB | fastq | 0.771 | 3 | 1.03 | 35.48× |

See `javascript/results.md`.

### csharp

| Size | First | Spearman | Flips | Time × | Spread |
|------|-------|---------:|------:|-------:|-------:|
| 1 B | ConcurrentQueue | 0.900 | 1 | 1.01 | 4.07× |
| 64 B | ConcurrentQueue | 0.900 | 1 | 1.07 | 4.03× |
| 256 B | ConcurrentQueue | 1.000 | 0 | 1.00 | 4.21× |
| 4 KiB | ConcurrentQueue | 1.000 | 0 | 0.91 | 4.62× |
| 64 KiB | ConcurrentQueue | 1.000 | 0 | 0.98 | 6.25× |

See `csharp/results.md`.

### c

| Size | First | Spearman | Flips | Time × | Spread |
|------|-------|---------:|------:|-------:|-------:|
| 1 B | spsc-ring | 0.949 | 1 | 0.97 | 14.47× |
| 64 B | spsc-ring | 0.800 | 1 | 1.00 | 14.48× |
| 256 B | spsc-ring | 1.000 | 0 | 1.00 | 14.47× |
| 4 KiB | spsc-ring | 1.000 | 0 | 0.99 | 14.83× |
| 64 KiB | spsc-ring | 0.800 | 1 | 0.98 | 14.48× |

See `c/results.md`.
