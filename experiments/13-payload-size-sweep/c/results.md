# c

Times are not comparable across languages.

## size_1 (1 B)

vs 256 B: Spearman 0.949, Kendall 1.000, 1 pairwise flip(s), time × 0.97.
Flips: steal-deque vs mutex-queue.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| spsc-ring | 944 | 1.00× | 99 |
| mutex-queue | 1294 | 1.37× | 99 |
| steal-deque | 1294 | 1.37× | 99 |
| lfqueue | 13664 | 14.47× | 99 |

## size_64 (64 B)

vs 256 B: Spearman 0.800, Kendall 0.667, 1 pairwise flip(s), time × 1.00.
Flips: steal-deque vs mutex-queue.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| spsc-ring | 968 | 1.00× | 99 |
| mutex-queue | 1326 | 1.37× | 99 |
| steal-deque | 1329 | 1.37× | 99 |
| lfqueue | 14021 | 14.48× | 99 |

## size_256 (256 B)

vs 256 B: Spearman 1.000, Kendall 1.000, 0 pairwise flip(s), time × 1.00.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| spsc-ring | 969 | 1.00× | 99 |
| steal-deque | 1333 | 1.38× | 99 |
| mutex-queue | 1334 | 1.38× | 99 |
| lfqueue | 14020 | 14.47× | 99 |

## size_4096 (4 KiB)

vs 256 B: Spearman 1.000, Kendall 1.000, 0 pairwise flip(s), time × 0.99.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| spsc-ring | 944 | 1.00× | 99 |
| steal-deque | 1290 | 1.37× | 99 |
| mutex-queue | 1326 | 1.40× | 99 |
| lfqueue | 13996 | 14.83× | 99 |

## size_65536 (64 KiB)

vs 256 B: Spearman 0.800, Kendall 0.667, 1 pairwise flip(s), time × 0.98.
Flips: steal-deque vs mutex-queue.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| spsc-ring | 944 | 1.00× | 99 |
| mutex-queue | 1292 | 1.37× | 99 |
| steal-deque | 1300 | 1.38× | 99 |
| lfqueue | 13671 | 14.48× | 99 |
