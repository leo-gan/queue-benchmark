using System.Collections.Concurrent;
using System.Diagnostics;
using System.Text;
using System.Threading.Channels;

var reps = args.Length > 0 && int.TryParse(args[0], out var r) ? r : 10;
var qf = args.Length > 1 ? args[1] : "";
var df = args.Length > 2 ? args[2] : "";

var special = Environment.GetEnvironmentVariable("BENCHMARK_SPECIAL") ?? "";

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
sb.AppendLine("Language,StringOrStream,TestDataName,Repetitions,RepetitionIndex,SerializerName,SerializerVersion,TimeSer,TimeDeser,Size,TimeSerAndDeser,OpPerSecSer,OpPerSecDeser,OpPerSecSerAndDeser,MemoryPeakBytes,FidelityScore,DataTypeInstanceCount,TypeConfigHash,SizeGzip,SizeZstd,NativeKind,StreamMode,RunOrder,SchedulePosition,CpuTimeNs");

string Ver = Environment.Version.ToString();
double Ops(long ns) => ns > 0 ? 1_000_000_000.0 / ns : 0;
int order = 0;
static (int p, int c) ParsePattern(string mode)
{
    mode = mode.ToLowerInvariant();
    if (mode is "bytes" or "spsc" or "string") return (1, 1);
    if (mode is "stream" or "mpmc") return (2, 2);
    var m = System.Text.RegularExpressions.Regex.Match(mode, @"^(\d+)p(\d+)c$");
    if (m.Success) return (int.Parse(m.Groups[1].Value), int.Parse(m.Groups[2].Value));
    return (1, 1);
}

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
        var (producers, consumers) = ParsePattern(cell.Mode);
        if (name == "Queue+lock" && (producers > 1 || consumers > 1))
            continue;
        if (special == "cancel" && name != "Channel")
            continue;
        for (int i = 0; i < reps; i++)
        {
            var proc = Process.GetCurrentProcess();
            var cpu0 = proc.TotalProcessorTime;
            var (enq, deq) = special switch
            {
                "wakeup" => BenchWakeup(items.Length),
                "burst" => name switch
                {
                    "Queue+lock" => BenchLocked(items),
                    "ConcurrentQueue" => BenchConcurrent(items, 1, 1),
                    "Channel" => BenchChannel(items, 1, 1).GetAwaiter().GetResult(),
                    _ => (0L, 0L)
                },
                "cancel" => BenchCancel(Math.Max(8, items.Length)).GetAwaiter().GetResult(),
                _ => name switch
                {
                    "Queue+lock" => BenchLocked(items),
                    "ConcurrentQueue" => BenchConcurrent(items, producers, consumers),
                    "Channel" => BenchChannel(items, producers, consumers).GetAwaiter().GetResult(),
                    _ => (0L, 0L)
                }
            };
            var cpuNs = (long)((proc.TotalProcessorTime - cpu0).TotalNanoseconds);
            var tot = enq + deq;
            var kind = name == "Channel" ? "async" : name == "ConcurrentQueue" ? "concurrent" : "locked";
            sb.AppendLine(string.Join(",",
                "csharp", cell.Mode, cell.Type, reps, i, name, Ver,
                enq, deq, size, tot,
                Ops(enq).ToString("F6"), Ops(deq).ToString("F6"), Ops(tot).ToString("F6"),
                0, "1.0000", cell.N, cell.Hash, 0, 0, kind,
                cell.Mode == "stream" ? "native" : "", order, order, cpuNs));
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

static (long enq, long deq) BenchConcurrent(byte[][] items, int producers, int consumers)
{
    var q = new ConcurrentQueue<byte[]>();
    if (producers == 1 && consumers == 1)
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
    var n = items.Length;
    var tasks = new List<Task>();
    var sw2 = Stopwatch.StartNew();
    for (int p = 0; p < producers; p++)
    {
        var a = n * p / producers;
        var b = n * (p + 1) / producers;
        tasks.Add(Task.Run(() => { for (int i = a; i < b; i++) q.Enqueue(items[i]); }));
    }
    var got = 0;
    for (int c = 0; c < consumers; c++)
    {
        tasks.Add(Task.Run(() =>
        {
            while (Volatile.Read(ref got) < n)
            {
                if (q.TryDequeue(out _)) Interlocked.Increment(ref got);
            }
        }));
    }
    Task.WaitAll(tasks.ToArray());
    var wall = (long)sw2.Elapsed.TotalNanoseconds;
    return (wall / 2, wall - wall / 2);
}

static async Task<(long enq, long deq)> BenchChannel(byte[][] items, int producers, int consumers)
{
    var ch = Channel.CreateUnbounded<byte[]>();
    if (producers == 1 && consumers == 1)
    {
        var sw = Stopwatch.StartNew();
        foreach (var it in items) await ch.Writer.WriteAsync(it);
        ch.Writer.Complete();
        var enq = (long)sw.Elapsed.TotalNanoseconds;
        sw.Restart();
        await foreach (var _ in ch.Reader.ReadAllAsync()) { }
        return (enq, (long)sw.Elapsed.TotalNanoseconds);
    }
    var n = items.Length;
    var sw2 = Stopwatch.StartNew();
    var writers = Enumerable.Range(0, producers).Select(p => Task.Run(async () =>
    {
        var a = n * p / producers;
        var b = n * (p + 1) / producers;
        for (int i = a; i < b; i++) await ch.Writer.WriteAsync(items[i]);
    }));
    var got = 0;
    var readers = Enumerable.Range(0, consumers).Select(_ => Task.Run(async () =>
    {
        while (Volatile.Read(ref got) < n)
        {
            if (ch.Reader.TryRead(out byte[] _)) Interlocked.Increment(ref got);
            else await Task.Yield();
        }
    }));
    await Task.WhenAll(writers.Concat(readers));
    var wall = (long)sw2.Elapsed.TotalNanoseconds;
    return (wall / 2, wall - wall / 2);
}

static (long enq, long deq) BenchWakeup(int n)
{
    n = Math.Max(1, n);
    var waitNs = 1_000_000L;
    var env = Environment.GetEnvironmentVariable("BENCHMARK_WAIT_NS");
    if (!string.IsNullOrEmpty(env) && long.TryParse(env, out var parsed))
        waitNs = parsed;
    var bag = new BlockingCollection<byte[]>(boundedCapacity: 1);
    var h = Task.Run(() =>
    {
        for (int i = 0; i < n; i++)
            bag.Take();
    });
    Thread.Sleep(2);
    var sw = Stopwatch.StartNew();
    for (int i = 0; i < n; i++)
    {
        var ms = (int)(waitNs / 1_000_000);
        if (ms > 0) Thread.Sleep(ms);
        else Thread.SpinWait(50);
        bag.Add(new byte[] { 1 });
    }
    h.Wait();
    var wall = (long)sw.Elapsed.TotalNanoseconds;
    return (wall / n, wall - wall / n);
}

static async Task<(long enq, long deq)> BenchCancel(int waiters)
{
    var ch = Channel.CreateUnbounded<byte[]>();
    using var cts = new CancellationTokenSource();
    var tasks = Enumerable.Range(0, Math.Max(8, waiters)).Select(_ => Task.Run(async () =>
    {
        try { await ch.Reader.ReadAsync(cts.Token); }
        catch (OperationCanceledException) { }
    })).ToArray();
    await Task.Delay(1);
    var sw = Stopwatch.StartNew();
    cts.Cancel();
    await Task.WhenAll(tasks);
    return ((long)sw.Elapsed.TotalNanoseconds, 0);
}
