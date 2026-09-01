# csharp

Times are not comparable across languages.

## size_1 (1 B)

vs 256 B: Spearman 0.900, Kendall 0.800, 1 pairwise flip(s), time × 1.01.
Flips: steal-deque vs BlockingCollection.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 3000 | 1.00× | 99 |
| Queue+lock | 5900 | 1.97× | 99 |
| BlockingCollection | 9200 | 3.07× | 99 |
| steal-deque | 9400 | 3.13× | 99 |
| Channel | 12200 | 4.07× | 99 |

## size_64 (64 B)

vs 256 B: Spearman 0.900, Kendall 0.800, 1 pairwise flip(s), time × 1.07.
Flips: steal-deque vs BlockingCollection.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 3100 | 1.00× | 99 |
| Queue+lock | 7400 | 2.39× | 99 |
| BlockingCollection | 9600 | 3.10× | 99 |
| steal-deque | 9900 | 3.19× | 99 |
| Channel | 12500 | 4.03× | 99 |

## size_256 (256 B)

vs 256 B: Spearman 1.000, Kendall 1.000, 0 pairwise flip(s), time × 1.00.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 2900 | 1.00× | 99 |
| Queue+lock | 6200 | 2.14× | 99 |
| steal-deque | 8900 | 3.07× | 99 |
| BlockingCollection | 9100 | 3.14× | 99 |
| Channel | 12200 | 4.21× | 99 |

## size_4096 (4 KiB)

vs 256 B: Spearman 1.000, Kendall 1.000, 0 pairwise flip(s), time × 0.91.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 2600 | 1.00× | 99 |
| Queue+lock | 5100 | 1.96× | 99 |
| steal-deque | 8100 | 3.12× | 99 |
| BlockingCollection | 8900 | 3.42× | 99 |
| Channel | 12000 | 4.62× | 99 |

## size_65536 (64 KiB)

vs 256 B: Spearman 1.000, Kendall 1.000, 0 pairwise flip(s), time × 0.98.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| ConcurrentQueue | 2800 | 1.00× | 99 |
| Queue+lock | 4900 | 1.75× | 99 |
| steal-deque | 8700 | 3.11× | 99 |
| BlockingCollection | 10800 | 3.86× | 99 |
| Channel | 17500 | 6.25× | 99 |
