# rust

Times are not comparable across languages.

## size_1 (1 B)

vs 256 B: Spearman 0.786, Kendall 0.714, 3 pairwise flip(s), time × 0.99.
Flips: std-mpsc vs flume; std-mpsc vs crossbeam-channel; std-mpsc vs tokio-mpsc.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| crossbeam-queue | 4107 | 1.00× | 99 |
| steal-deque | 4425 | 1.08× | 99 |
| flume | 6472 | 1.58× | 99 |
| crossbeam-channel | 6834 | 1.66× | 99 |
| tokio-mpsc | 7745 | 1.89× | 99 |
| std-mpsc | 9546 | 2.32× | 99 |
| async-channel | 10470 | 2.55× | 99 |

## size_64 (64 B)

vs 256 B: Spearman 0.964, Kendall 0.905, 1 pairwise flip(s), time × 0.84.
Flips: std-mpsc vs flume.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| crossbeam-queue | 4542 | 1.00× | 99 |
| steal-deque | 4601 | 1.01× | 99 |
| flume | 4887 | 1.08× | 99 |
| std-mpsc | 4902 | 1.08× | 99 |
| crossbeam-channel | 5634 | 1.24× | 99 |
| tokio-mpsc | 6164 | 1.36× | 99 |
| async-channel | 10891 | 2.40× | 99 |

## size_256 (256 B)

vs 256 B: Spearman 1.000, Kendall 1.000, 0 pairwise flip(s), time × 1.00.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| crossbeam-queue | 5350 | 1.00× | 99 |
| steal-deque | 5446 | 1.02× | 99 |
| std-mpsc | 6019 | 1.13× | 99 |
| flume | 6546 | 1.22× | 99 |
| crossbeam-channel | 6762 | 1.26× | 99 |
| tokio-mpsc | 7304 | 1.37× | 99 |
| async-channel | 11474 | 2.14× | 99 |

## size_4096 (4 KiB)

vs 256 B: Spearman 0.750, Kendall 0.619, 4 pairwise flip(s), time × 9.24.
Flips: crossbeam-queue vs steal-deque; crossbeam-queue vs flume; steal-deque vs flume; std-mpsc vs flume.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| flume | 59130 | 1.00× | 99 |
| steal-deque | 59582 | 1.01× | 99 |
| crossbeam-queue | 61833 | 1.05× | 99 |
| std-mpsc | 62230 | 1.05× | 99 |
| crossbeam-channel | 62478 | 1.06× | 99 |
| tokio-mpsc | 65210 | 1.10× | 99 |
| async-channel | 70093 | 1.19× | 99 |

## size_65536 (64 KiB)

vs 256 B: Spearman -0.357, Kendall -0.238, 13 pairwise flip(s), time × 282.37.
Flips: crossbeam-queue vs steal-deque; crossbeam-queue vs std-mpsc; crossbeam-queue vs flume; crossbeam-queue vs crossbeam-channel; crossbeam-queue vs tokio-mpsc; crossbeam-queue vs async-channel; steal-deque vs std-mpsc; steal-deque vs flume; steal-deque vs crossbeam-channel; steal-deque vs tokio-mpsc; steal-deque vs async-channel; flume vs crossbeam-channel; tokio-mpsc vs async-channel.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| std-mpsc | 1564000 | 1.00× | 99 |
| crossbeam-channel | 1755998 | 1.12× | 99 |
| flume | 1944333 | 1.24× | 99 |
| async-channel | 1963145 | 1.26× | 99 |
| tokio-mpsc | 2062398 | 1.32× | 99 |
| steal-deque | 2096368 | 1.34× | 99 |
| crossbeam-queue | 2113792 | 1.35× | 99 |
