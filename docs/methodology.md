# Methodology

To reach the quality of a scientific data science paper, we employ robust statistics to measure queue performance:
- **Mean & Std Dev (ns)**
- **Min, Max, p50, p95, p99 (ns)**
- **Throughput (Ops/sec and MB/sec)**

Measurements discard startup cost overhead when possible and measure individual enqueues/dequeues.
