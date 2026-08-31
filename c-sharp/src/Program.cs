using System.Collections.Concurrent;
using System.Diagnostics;
using System.Text;
using System.Threading.Channels;

var reps = args.Length > 0 && int.TryParse(args[0], out var r) ? r : 10;
var qf = args.Length > 1 ? args[1] : "";
var df = args.Length > 2 ? args[2] : "";

var cellsPath = Environment.GetEnvironmentVariable("BENCHMARK_CELLS_TSV") ?? "cells.tsv";
var cells = File.ReadAllLines(cellsPath).Skip(1)
    .Select(ln => ln.Split('\t'))
    .Where(p => p.Length >= 5)
    .Select(p => (Type: p[0], Payload: int.Parse(p[1]), N: int.Parse(p[2]), Mode: p[3], Hash: p[4]))
    .ToList();

var logDir = Environment.GetEnvironmentVariable("LOG_DIR") ?? "../logs/csharp";
if (!logDir.EndsWith("csharp") && !logDir.EndsWith("csharp/"))
    logDir = Path.Combine(logDir, "csharp");
Directory.CreateDirectory(logDir);
var stamp = Environment.GetEnvironmentVariable("BENCHMARK_TS") ?? "run";
var csv = Path.Combine(logDir, stamp + ".csv");
var sb = new StringBuilder();
sb.AppendLine("Language,StringOrStream,TestDataName,Repetitions,RepetitionIndex,SerializerName,SerializerVersion,TimeSer,TimeDeser,Size,TimeSerAndDeser,OpPerSecSer,OpPerSecDeser,OpPerSecSerAndDeser,MemoryPeakBytes,FidelityScore,DataTypeInstanceCount,TypeConfigHash,SizeGzip,SizeZstd,NativeKind,StreamMode,RunOrder,SchedulePosition");

string Ver = Environment.Version.ToString();
double Ops(long ns) => ns > 0 ? 1_000_000_000.0 / ns : 0;
int order = 0;
string[] queues = ["Queue+lock", "ConcurrentQueue", "Channel"];

foreach (var cell in cells)
{
    if (df.Length > 0 && !cell.Type.Contains(df, StringComparison.OrdinalIgnoreCase))
        continue;
    var item = new byte[cell.Payload];
    for (int i = 0; i < item.Length; i++) item[i] = (byte)(i % 251);
    var items = Enumerable.Repeat(item, cell.N).ToArray();
    var size = cell.Payload * cell.N;
    foreach (var name in queues)
    {
        if (qf.Length > 0 && !name.Contains(qf, StringComparison.OrdinalIgnoreCase))
            continue;
        for (int i = 0; i < reps; i++)
        {
            var (enq, deq) = name switch
            {
                "Queue+lock" => BenchLocked(items),
                "ConcurrentQueue" => BenchConcurrent(items, cell.Mode == "stream"),
                "Channel" => BenchChannel(items).GetAwaiter().GetResult(),
                _ => (0L, 0L)
            };
            var tot = enq + deq;
            var kind = name == "Channel" ? "async" : name == "ConcurrentQueue" ? "concurrent" : "locked";
            sb.AppendLine(string.Join(",",
                "csharp", cell.Mode, cell.Type, reps, i, name, Ver,
                enq, deq, size, tot,
                Ops(enq).ToString("F6"), Ops(deq).ToString("F6"), Ops(tot).ToString("F6"),
                0, "1.0000", cell.N, cell.Hash, 0, 0, kind,
                cell.Mode == "stream" ? "native" : "", order, order));
            order++;
        }
    }
}

File.WriteAllText(csv, sb.ToString());
Console.WriteLine("Wrote " + csv);

static (long enq, long deq) BenchLocked(byte[][] items)
{
    var q = new Queue<byte[]>();
    var gate = new object();
    var sw = Stopwatch.StartNew();
    foreach (var it in items)
    {
        lock (gate) q.Enqueue(it);
    }
    var enq = (long)(sw.Elapsed.TotalNanoseconds);
    sw.Restart();
    foreach (var _ in items)
    {
        lock (gate) q.Dequeue();
    }
    return (enq, (long)sw.Elapsed.TotalNanoseconds);
}

static (long enq, long deq) BenchConcurrent(byte[][] items, bool mpmc)
{
    var q = new ConcurrentQueue<byte[]>();
    if (!mpmc)
    {
        var sw = Stopwatch.StartNew();
        foreach (var it in items) q.Enqueue(it);
        var enq = (long)sw.Elapsed.TotalNanoseconds;
        sw.Restart();
        for (int i = 0; i < items.Length; i++)
        {
            while (!q.TryDequeue(out _)) { }
        }
        return (enq, (long)sw.Elapsed.TotalNanoseconds);
    }
    var half = items.Length / 2;
    var sw2 = Stopwatch.StartNew();
    var p1 = Task.Run(() => { for (int i = 0; i < half; i++) q.Enqueue(items[i]); });
    var p2 = Task.Run(() => { for (int i = half; i < items.Length; i++) q.Enqueue(items[i]); });
    var got = 0;
    var c1 = Task.Run(() =>
    {
        while (Volatile.Read(ref got) < items.Length)
        {
            if (q.TryDequeue(out _)) Interlocked.Increment(ref got);
        }
    });
    var c2 = Task.Run(() =>
    {
        while (Volatile.Read(ref got) < items.Length)
        {
            if (q.TryDequeue(out _)) Interlocked.Increment(ref got);
        }
    });
    Task.WaitAll(p1, p2, c1, c2);
    var wall = (long)sw2.Elapsed.TotalNanoseconds;
    return (wall / 2, wall - wall / 2);
}

static async Task<(long enq, long deq)> BenchChannel(byte[][] items)
{
    var ch = Channel.CreateUnbounded<byte[]>();
    var sw = Stopwatch.StartNew();
    foreach (var it in items) await ch.Writer.WriteAsync(it);
    ch.Writer.Complete();
    var enq = (long)sw.Elapsed.TotalNanoseconds;
    sw.Restart();
    await foreach (var _ in ch.Reader.ReadAllAsync()) { }
    return (enq, (long)sw.Elapsed.TotalNanoseconds);
}
