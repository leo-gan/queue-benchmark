import math
import json

def calculate_stats(times_ns, total_bytes):
    if not times_ns:
        return {}

    times_ns.sort()
    n = len(times_ns)

    # Calculate stats in nanoseconds
    mean_ns = sum(times_ns) / n
    variance_ns = sum((x - mean_ns) ** 2 for x in times_ns) / n
    stddev_ns = math.sqrt(variance_ns)

    min_ns = times_ns[0]
    max_ns = times_ns[-1]
    p50_ns = times_ns[int(n * 0.50)]
    p95_ns = times_ns[int(n * 0.95)]
    p99_ns = times_ns[int(n * 0.99)]

    total_time_s = sum(times_ns) / 1e9
    throughput_ops = n / total_time_s if total_time_s > 0 else 0
    throughput_mb = (total_bytes / (1024 * 1024)) / total_time_s if total_time_s > 0 else 0

    return {
        "mean_ns": mean_ns,
        "stddev_ns": stddev_ns,
        "min_ns": min_ns,
        "max_ns": max_ns,
        "p50_ns": p50_ns,
        "p95_ns": p95_ns,
        "p99_ns": p99_ns,
        "throughput_ops_sec": throughput_ops,
        "throughput_mb_sec": throughput_mb
    }

def print_stats(queue_name, stats_dict):
    print(json.dumps({queue_name: stats_dict}, indent=2))
