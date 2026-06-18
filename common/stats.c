#include "stats.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

int compare_ull(const void *a, const void *b) {
    unsigned long long ua = *(const unsigned long long *)a;
    unsigned long long ub = *(const unsigned long long *)b;
    if (ua < ub) return -1;
    if (ua > ub) return 1;
    return 0;
}

StatsData calculate_stats(unsigned long long *times_ns, size_t n, size_t total_bytes) {
    StatsData stats = {0};
    if (n == 0) return stats;

    qsort(times_ns, n, sizeof(unsigned long long), compare_ull);

    unsigned long long sum_ns = 0;
    for (size_t i = 0; i < n; i++) sum_ns += times_ns[i];

    stats.mean_ns = (double)sum_ns / n;

    double variance_ns = 0;
    for (size_t i = 0; i < n; i++) {
        double diff = times_ns[i] - stats.mean_ns;
        variance_ns += diff * diff;
    }
    variance_ns /= n;
    stats.stddev_ns = sqrt(variance_ns);

    stats.min_ns = times_ns[0];
    stats.max_ns = times_ns[n - 1];
    stats.p50_ns = times_ns[(size_t)(n * 0.50)];
    stats.p95_ns = times_ns[(size_t)(n * 0.95)];
    stats.p99_ns = times_ns[(size_t)(n * 0.99)];

    double total_time_s = sum_ns / 1e9;
    if (total_time_s > 0) {
        stats.throughput_ops_sec = n / total_time_s;
        stats.throughput_mb_sec = ((double)total_bytes / (1024.0 * 1024.0)) / total_time_s;
    }

    return stats;
}

void print_stats(const char *queue_name, StatsData stats) {
    printf("{\n");
    printf("  \"%s\": {\n", queue_name);
    printf("    \"mean_ns\": %f,\n", stats.mean_ns);
    printf("    \"stddev_ns\": %f,\n", stats.stddev_ns);
    printf("    \"min_ns\": %f,\n", stats.min_ns);
    printf("    \"max_ns\": %f,\n", stats.max_ns);
    printf("    \"p50_ns\": %f,\n", stats.p50_ns);
    printf("    \"p95_ns\": %f,\n", stats.p95_ns);
    printf("    \"p99_ns\": %f,\n", stats.p99_ns);
    printf("    \"throughput_ops_sec\": %f,\n", stats.throughput_ops_sec);
    printf("    \"throughput_mb_sec\": %f\n", stats.throughput_mb_sec);
    printf("  }\n");
    printf("}\n");
}
