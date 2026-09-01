# python

Times are not comparable across languages.

## size_1 (1 B)

vs 256 B: Spearman 1.000, Kendall 1.000, 0 pairwise flip(s), time × 0.94.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | 6360 | 1.00× | 99 |
| spsc-ring | 15263 | 2.40× | 99 |
| deque-lock | 18062 | 2.84× | 99 |
| steal-deque | 20020 | 3.15× | 99 |
| asyncio.Queue | 43637 | 6.86× | 99 |
| queue.Queue | 52988 | 8.33× | 99 |
| janus | 105187 | 16.54× | 99 |

## size_64 (64 B)

vs 256 B: Spearman 0.964, Kendall 0.905, 1 pairwise flip(s), time × 0.98.
Flips: deque-lock vs steal-deque.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | 6750 | 1.00× | 99 |
| spsc-ring | 15177 | 2.25× | 99 |
| steal-deque | 19446 | 2.88× | 99 |
| deque-lock | 19924 | 2.95× | 99 |
| asyncio.Queue | 45670 | 6.77× | 99 |
| queue.Queue | 58876 | 8.72× | 99 |
| janus | 107444 | 15.92× | 99 |

## size_256 (256 B)

vs 256 B: Spearman 1.000, Kendall 1.000, 0 pairwise flip(s), time × 1.00.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | 6755 | 1.00× | 99 |
| spsc-ring | 16353 | 2.42× | 99 |
| deque-lock | 19305 | 2.86× | 99 |
| steal-deque | 19920 | 2.95× | 99 |
| asyncio.Queue | 46617 | 6.90× | 99 |
| queue.Queue | 58004 | 8.59× | 99 |
| janus | 110450 | 16.35× | 99 |

## size_4096 (4 KiB)

vs 256 B: Spearman 1.000, Kendall 1.000, 0 pairwise flip(s), time × 1.07.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | 7251 | 1.00× | 99 |
| spsc-ring | 18716 | 2.58× | 99 |
| deque-lock | 19357 | 2.67× | 99 |
| steal-deque | 22783 | 3.14× | 99 |
| asyncio.Queue | 47305 | 6.52× | 99 |
| queue.Queue | 58309 | 8.04× | 99 |
| janus | 118035 | 16.28× | 99 |

## size_65536 (64 KiB)

vs 256 B: Spearman 1.000, Kendall 1.000, 0 pairwise flip(s), time × 1.17.

| Library | Median handoff (ns) | vs fastest | n |
|---------|--------------------:|-----------:|--:|
| queue.SimpleQueue | 7821 | 1.00× | 99 |
| spsc-ring | 19707 | 2.52× | 99 |
| deque-lock | 23091 | 2.95× | 99 |
| steal-deque | 23530 | 3.01× | 99 |
| asyncio.Queue | 53915 | 6.89× | 99 |
| queue.Queue | 66819 | 8.54× | 99 |
| janus | 128735 | 16.46× | 99 |
