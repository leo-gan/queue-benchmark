using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json;

namespace Common
{
    public class StatsData
    {
        public double mean_ns { get; set; }
        public double stddev_ns { get; set; }
        public double min_ns { get; set; }
        public double max_ns { get; set; }
        public double p50_ns { get; set; }
        public double p95_ns { get; set; }
        public double p99_ns { get; set; }
        public double throughput_ops_sec { get; set; }
        public double throughput_mb_sec { get; set; }
    }

    public static class Stats
    {
        public static StatsData Calculate(List<long> times_ns, long totalBytes)
        {
            if (times_ns == null || times_ns.Count == 0) return new StatsData();

            times_ns.Sort();
            int n = times_ns.Count;

            double mean_ns = times_ns.Average();
            double variance_ns = times_ns.Select(val => (val - mean_ns) * (val - mean_ns)).Sum() / n;
            double stddev_ns = Math.Sqrt(variance_ns);

            double total_time_s = times_ns.Sum() / 1e9;

            return new StatsData
            {
                mean_ns = mean_ns,
                stddev_ns = stddev_ns,
                min_ns = times_ns.First(),
                max_ns = times_ns.Last(),
                p50_ns = times_ns[(int)(n * 0.50)],
                p95_ns = times_ns[(int)(n * 0.95)],
                p99_ns = times_ns[(int)(n * 0.99)],
                throughput_ops_sec = total_time_s > 0 ? n / total_time_s : 0,
                throughput_mb_sec = total_time_s > 0 ? (totalBytes / (1024.0 * 1024.0)) / total_time_s : 0
            };
        }

        public static void Print(string queueName, StatsData stats)
        {
            var dict = new Dictionary<string, StatsData> { { queueName, stats } };
            Console.WriteLine(JsonSerializer.Serialize(dict, new JsonSerializerOptions { WriteIndented = true }));
        }
    }
}
