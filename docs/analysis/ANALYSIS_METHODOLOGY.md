# Analysis methodology

The analysis package (`analyze-benchmarks`) never rewrites raw logs.

1. **Load** the latest `logs/<lang>/*.csv` (or an explicit stem).
2. **Drop warmup** when `statistics.exclude_warmup` is true (index `< warmup_repetitions`).
3. **Outliers**: IQR with `k=1.5` (configurable). Raw rows stay in the CSV.
4. **Summaries**: mean, median, std, MAD, CV, percentiles, min/max.
5. **Bootstrap** 95% CI on the mean (percentile, 2000 iterations, seed 42).
6. **Rank** by `total_median_ns` (handoff). Lower is better.
7. **Effect sizes** vs the fastest in the group (Cliff’s δ, Hedges’ g).
8. **Regression gate**: fail only when the point estimate *and* the optimistic
   CI end are both more than `threshold_percent` slower than baseline.

Compare queues inside one language (and ideally one category).
