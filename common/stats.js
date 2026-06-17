function calculateStats(times_ns, totalBytes) {
    if (!times_ns || times_ns.length === 0) return {};

    times_ns.sort((a, b) => a - b);
    const n = times_ns.length;

    const sum_ns = times_ns.reduce((a, b) => a + b, 0);
    const mean_ns = sum_ns / n;

    const variance_ns = times_ns.reduce((a, b) => a + Math.pow(b - mean_ns, 2), 0) / n;
    const stddev_ns = Math.sqrt(variance_ns);

    const total_time_s = sum_ns / 1e9;

    return {
        mean_ns,
        stddev_ns,
        min_ns: times_ns[0],
        max_ns: times_ns[n - 1],
        p50_ns: times_ns[Math.floor(n * 0.50)],
        p95_ns: times_ns[Math.floor(n * 0.95)],
        p99_ns: times_ns[Math.floor(n * 0.99)],
        throughput_ops_sec: total_time_s > 0 ? n / total_time_s : 0,
        throughput_mb_sec: total_time_s > 0 ? (totalBytes / (1024 * 1024)) / total_time_s : 0
    };
}

function printStats(queueName, stats) {
    console.log(JSON.stringify({ [queueName]: stats }, null, 2));
}

module.exports = { calculateStats, printStats };
