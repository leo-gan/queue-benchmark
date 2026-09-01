# javascript

Times are not comparable across languages.

## size_1 (1 B)

vs 256 B: Spearman 0.829, Kendall 0.733, 2 pairwise flip(s), time × 2.14.
Flips: Array vs steal-deque; Array vs yocto-queue.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| fastq | 1473 | 1.00× | 99 |
| denque | 3539 | 2.40× | 99 |
| steal-deque | 6797 | 4.61× | 99 |
| yocto-queue | 7600 | 5.16× | 99 |
| Array | 8629 | 5.86× | 99 |
| p-queue | 60642 | 41.17× | 99 |

## size_64 (64 B)

vs 256 B: Spearman 0.829, Kendall 0.733, 2 pairwise flip(s), time × 0.99.
Flips: denque vs Array; denque vs steal-deque.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| fastq | 1388 | 1.00× | 99 |
| Array | 2520 | 1.82× | 99 |
| steal-deque | 2811 | 2.03× | 99 |
| denque | 3094 | 2.23× | 99 |
| yocto-queue | 3477 | 2.51× | 99 |
| p-queue | 62336 | 44.91× | 99 |

## size_256 (256 B)

vs 256 B: Spearman 1.000, Kendall 1.000, 0 pairwise flip(s), time × 1.00.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| fastq | 1404 | 1.00× | 99 |
| denque | 2680 | 1.91× | 99 |
| Array | 2697 | 1.92× | 99 |
| steal-deque | 2980 | 2.12× | 99 |
| yocto-queue | 3556 | 2.53× | 99 |
| p-queue | 45134 | 32.15× | 99 |

## size_4096 (4 KiB)

vs 256 B: Spearman 0.899, Kendall 0.857, 1 pairwise flip(s), time × 1.03.
Flips: Array vs steal-deque.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| fastq | 1200 | 1.00× | 99 |
| denque | 2839 | 2.37× | 99 |
| steal-deque | 2839 | 2.37× | 99 |
| Array | 2941 | 2.45× | 99 |
| yocto-queue | 3654 | 3.04× | 99 |
| p-queue | 43584 | 36.32× | 99 |

## size_65536 (64 KiB)

vs 256 B: Spearman 0.771, Kendall 0.600, 3 pairwise flip(s), time × 1.03.
Flips: denque vs Array; denque vs steal-deque; Array vs steal-deque.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| fastq | 1233 | 1.00× | 99 |
| steal-deque | 2825 | 2.29× | 99 |
| Array | 2985 | 2.42× | 99 |
| denque | 3043 | 2.47× | 99 |
| yocto-queue | 3674 | 2.98× | 99 |
| p-queue | 43742 | 35.48× | 99 |
