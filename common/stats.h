#ifndef STATS_H
#define STATS_H

#include <stddef.h>

typedef struct {
    double mean_ns;
    double stddev_ns;
    double min_ns;
    double max_ns;
    double p50_ns;
    double p95_ns;
    double p99_ns;
    double throughput_ops_sec;
    double throughput_mb_sec;
} StatsData;

StatsData calculate_stats(unsigned long long *times_ns, size_t n, size_t total_bytes);
void print_stats(const char *queue_name, StatsData stats);

#endif
