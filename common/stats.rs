use serde::Serialize;

#[derive(Serialize)]
pub struct StatsData {
    pub mean_ns: f64,
    pub stddev_ns: f64,
    pub min_ns: f64,
    pub max_ns: f64,
    pub p50_ns: f64,
    pub p95_ns: f64,
    pub p99_ns: f64,
    pub throughput_ops_sec: f64,
    pub throughput_mb_sec: f64,
}

pub fn calculate_stats(mut times_ns: Vec<u64>, total_bytes: usize) -> StatsData {
    if times_ns.is_empty() {
        return StatsData {
            mean_ns: 0.0, stddev_ns: 0.0, min_ns: 0.0, max_ns: 0.0,
            p50_ns: 0.0, p95_ns: 0.0, p99_ns: 0.0, throughput_ops_sec: 0.0, throughput_mb_sec: 0.0
        };
    }

    times_ns.sort_unstable();
    let n = times_ns.len() as f64;

    let sum_ns: u64 = times_ns.iter().sum();
    let mean_ns = sum_ns as f64 / n;

    let variance_ns = times_ns.iter()
        .map(|&x| (x as f64 - mean_ns).powi(2))
        .sum::<f64>() / n;
    let stddev_ns = variance_ns.sqrt();

    let total_time_s = sum_ns as f64 / 1e9;

    StatsData {
        mean_ns,
        stddev_ns,
        min_ns: times_ns[0] as f64,
        max_ns: *times_ns.last().unwrap() as f64,
        p50_ns: times_ns[(n * 0.50) as usize] as f64,
        p95_ns: times_ns[(n * 0.95) as usize] as f64,
        p99_ns: times_ns[(n * 0.99) as usize] as f64,
        throughput_ops_sec: if total_time_s > 0.0 { n / total_time_s } else { 0.0 },
        throughput_mb_sec: if total_time_s > 0.0 { (total_bytes as f64 / (1024.0 * 1024.0)) / total_time_s } else { 0.0 }
    }
}

pub fn print_stats(queue_name: &str, stats: &StatsData) {
    let json = serde_json::json!({
        queue_name: stats
    });
    println!("{}", serde_json::to_string_pretty(&json).unwrap());
}
