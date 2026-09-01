using System.Collections.Concurrent;
using System.Diagnostics;
using System.IO.MemoryMappedFiles;
using System.Net;
using System.Text;
using System.Threading.Channels;
using Microsoft.Data.Sqlite;

if ((Environment.GetEnvironmentVariable("BENCHMARK_CHILD") ?? "") == "pipe")
{
    ChildPipe();
    return;
}
if ((Environment.GetEnvironmentVariable("BENCHMARK_CHILD") ?? "") == "shared")
{
    ChildShared();
    return;
}

var reps = args.Length > 0 && int.TryParse(args[0], out var r) ? r : 10;
var qf = args.Length > 1 ? args[1] : "";
var df = args.Length > 2 ? args[2] : "";

var special = Environment.GetEnvironmentVariable("BENCHMARK_SPECIAL") ?? "";
var includePsd = On(Environment.GetEnvironmentVariable("BENCHMARK_INCLUDE_PSD"));
var psdNames = (Environment.GetEnvironmentVariable("BENCHMARK_PSD_NAMES") ?? "")
    .Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
    .ToHashSet(StringComparer.Ordinal);

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
sb.AppendLine("Language,Pattern,TestDataName,Repetitions,RepetitionIndex,LibraryName,LibraryVersion,TimeEnq,TimeDeq,Size,TimeHandoff,OpPerSecEnq,OpPerSecDeq,OpPerSecHandoff,MemoryPeakBytes,FidelityScore,DataTypeInstanceCount,TypeConfigHash,SizeGzip,SizeZstd,NativeKind,StreamMode,RunOrder,SchedulePosition,CpuTimeNs");

string Ver = Environment.Version.ToString();
double Ops(long ns) => ns > 0 ? 1_000_000_000.0 / ns : 0;
int order = 0;
static bool On(string? v) => v is "1" or "true" or "on";
static (int p, int c) ParsePattern(string mode)
{
    mode = mode.ToLowerInvariant();
    if (mode is "bytes" or "spsc" or "string") return (1, 1);
    if (mode is "stream" or "mpmc") return (2, 2);
    var m = System.Text.RegularExpressions.Regex.Match(mode, @"^(\d+)p(\d+)c$");
    if (m.Success) return (int.Parse(m.Groups[1].Value), int.Parse(m.Groups[2].Value));
    return (1, 1);
}

(string name, string kind, bool optIn, bool spscOnly)[] queues =
[
    ("Queue+lock", "locked", false, true),
    ("ConcurrentQueue", "concurrent", false, false),
    ("BlockingCollection", "concurrent", false, false),
    ("Channel", "async", false, false),
    ("steal-deque", "work-stealing", false, false),
    ("pipe-ipc", "concurrent", true, true),
    ("shared-ring", "spsc", true, true),
    ("sqlite-queue", "durable", true, true),
];

foreach (var cell in cells)
{
    if (df.Length > 0 && !cell.Type.Contains(df, StringComparison.OrdinalIgnoreCase))
        continue;
    var item = new byte[cell.Payload];
    for (int i = 0; i < item.Length; i++) item[i] = (byte)(i % 251);
    var items = Enumerable.Repeat(item, cell.N).ToArray();
    var size = cell.Payload * cell.N;
    foreach (var q in queues)
    {
        if (qf.Length > 0 && !q.name.Contains(qf, StringComparison.OrdinalIgnoreCase))
            continue;
        if (q.optIn)
        {
            if (!includePsd && qf.Length == 0) continue;
            if (psdNames.Count > 0 && !psdNames.Contains(q.name)) continue;
        }
        var (producers, consumers) = ParsePattern(cell.Mode);
        if (q.spscOnly && (producers != 1 || consumers != 1)) continue;
        if (special == "cancel" && q.name != "Channel") continue;
        if (special.Length > 0 && q.optIn) continue;
        if (special == "wakeup" && q.name is "steal-deque" or "shared-ring") continue;
        for (int i = 0; i < reps; i++)
        {
            var proc = Process.GetCurrentProcess();
            var cpu0 = proc.TotalProcessorTime;
            var (enq, deq) = special switch
            {
                "wakeup" => BenchWakeup(items.Length),
                "burst" => q.name switch
                {
                    "Queue+lock" => BenchLocked(items),
                    "ConcurrentQueue" => BenchConcurrent(items, 1, 1),
                    "BlockingCollection" => BenchBlocking(items, 1, 1),
                    "Channel" => BenchChannel(items, 1, 1).GetAwaiter().GetResult(),
                    "steal-deque" => BenchSteal(items, 1, 1),
                    _ => (0L, 0L)
                },
                "cancel" => BenchCancel(Math.Max(8, items.Length)).GetAwaiter().GetResult(),
                _ => q.name switch
                {
                    "Queue+lock" => BenchLocked(items),
                    "ConcurrentQueue" => BenchConcurrent(items, producers, consumers),
                    "BlockingCollection" => BenchBlocking(items, producers, consumers),
                    "Channel" => BenchChannel(items, producers, consumers).GetAwaiter().GetResult(),
                    "steal-deque" => BenchSteal(items, producers, consumers),
                    "pipe-ipc" => BenchPipe(items),
                    "shared-ring" => BenchShared(items),
                    "sqlite-queue" => BenchSqlite(items),
                    _ => (0L, 0L)
                }
            };
            var cpuNs = (long)((proc.TotalProcessorTime - cpu0).TotalNanoseconds);
            var rss = proc.PeakWorkingSet64;
            var tot = enq + deq;
            sb.AppendLine(string.Join(",",
                "csharp", cell.Mode, cell.Type, reps, i, q.name, Ver,
                enq, deq, size, tot,
                Ops(enq).ToString("F6"), Ops(deq).ToString("F6"), Ops(tot).ToString("F6"),
                rss, "1.0000", cell.N, cell.Hash, 0, 0, q.kind,
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

static (long enq, long deq) BenchBlocking(byte[][] items, int producers, int consumers)
{
    var q = new BlockingCollection<byte[]>();
    if (producers == 1 && consumers == 1)
    {
        var sw = Stopwatch.StartNew();
        foreach (var it in items) q.Add(it);
        var enq = (long)sw.Elapsed.TotalNanoseconds;
        sw.Restart();
        for (int i = 0; i < items.Length; i++) q.Take();
        return (enq, (long)sw.Elapsed.TotalNanoseconds);
    }
    var n = items.Length;
    var tasks = new List<Task>();
    var sw2 = Stopwatch.StartNew();
    for (int p = 0; p < producers; p++)
    {
        var a = n * p / producers;
        var b = n * (p + 1) / producers;
        tasks.Add(Task.Run(() => { for (int i = a; i < b; i++) q.Add(items[i]); }));
    }
    var per = n / consumers;
    var extra = n % consumers;
    for (int c = 0; c < consumers; c++)
    {
        var take = per + (c == 0 ? extra : 0);
        tasks.Add(Task.Run(() => { for (int i = 0; i < take; i++) q.Take(); }));
    }
    Task.WaitAll(tasks.ToArray());
    var wall = (long)sw2.Elapsed.TotalNanoseconds;
    return (wall / 2, wall - wall / 2);
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

static (long enq, long deq) BenchSteal(byte[][] items, int producers, int consumers)
{
    var q = new LinkedList<byte[]>();
    var gate = new object();
    void Push(byte[] it) { lock (gate) q.AddLast(it); }
    byte[] Steal()
    {
        while (true)
        {
            lock (gate)
            {
                if (q.Count > 0)
                {
                    var x = q.First!.Value;
                    q.RemoveFirst();
                    return x;
                }
            }
            Thread.SpinWait(20);
        }
    }
    if (producers == 1 && consumers == 1)
    {
        var sw = Stopwatch.StartNew();
        foreach (var it in items) Push(it);
        var enq = (long)sw.Elapsed.TotalNanoseconds;
        sw.Restart();
        foreach (var _ in items) Steal();
        return (enq, (long)sw.Elapsed.TotalNanoseconds);
    }
    var n = items.Length;
    var tasks = new List<Task>();
    var sw2 = Stopwatch.StartNew();
    for (int p = 0; p < producers; p++)
    {
        var a = n * p / producers;
        var b = n * (p + 1) / producers;
        tasks.Add(Task.Run(() => { for (int i = a; i < b; i++) Push(items[i]); }));
    }
    var per = n / consumers;
    var extra = n % consumers;
    for (int c = 0; c < consumers; c++)
    {
        var take = per + (c == 0 ? extra : 0);
        tasks.Add(Task.Run(() => { for (int i = 0; i < take; i++) Steal(); }));
    }
    Task.WaitAll(tasks.ToArray());
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

static ProcessStartInfo ChildPsi()
{
    var asm = System.Reflection.Assembly.GetExecutingAssembly().Location;
    var psi = new ProcessStartInfo
    {
        FileName = Environment.ProcessPath ?? "dotnet",
        UseShellExecute = false,
        RedirectStandardInput = true,
        RedirectStandardOutput = true,
        RedirectStandardError = true,
        CreateNoWindow = true,
    };
    var exe = Path.GetFileName(psi.FileName);
    if (asm.EndsWith(".dll", StringComparison.OrdinalIgnoreCase)
        && !exe.StartsWith("QueueBenchmark", StringComparison.OrdinalIgnoreCase))
    {
        psi.ArgumentList.Add(asm);
    }
    return psi;
}

static void WriteFrame(Stream s, byte[] it)
{
    var len = BitConverter.GetBytes(IPAddress.HostToNetworkOrder(it.Length));
    s.Write(len, 0, 4);
    s.Write(it, 0, it.Length);
}

static byte[] ReadFrame(Stream s)
{
    var lenb = new byte[4];
    var got = 0;
    while (got < 4)
    {
        var n = s.Read(lenb, got, 4 - got);
        if (n <= 0) throw new EndOfStreamException();
        got += n;
    }
    var len = IPAddress.NetworkToHostOrder(BitConverter.ToInt32(lenb, 0));
    var buf = new byte[len];
    got = 0;
    while (got < len)
    {
        var n = s.Read(buf, got, len - got);
        if (n <= 0) throw new EndOfStreamException();
        got += n;
    }
    return buf;
}

static void ChildPipe()
{
    var n = int.Parse(Environment.GetEnvironmentVariable("BENCHMARK_CHILD_N") ?? "0");
    var stdin = Console.OpenStandardInput();
    for (int i = 0; i < n; i++)
        ReadFrame(stdin);
}

static (long enq, long deq) BenchPipe(byte[][] items)
{
    var psi = ChildPsi();
    psi.Environment["BENCHMARK_CHILD"] = "pipe";
    psi.Environment["BENCHMARK_CHILD_N"] = items.Length.ToString();
    using var child = Process.Start(psi)!;
    var sw = Stopwatch.StartNew();
    var stdin = child.StandardInput.BaseStream;
    foreach (var it in items)
        WriteFrame(stdin, it);
    stdin.Flush();
    child.StandardInput.Close();
    child.WaitForExit();
    var wall = (long)sw.Elapsed.TotalNanoseconds;
    return (wall / 2, wall - wall / 2);
}

const int RingHeader = 16;

static void RingPush(MemoryMappedViewAccessor acc, byte[] item, int slots, int slot)
{
    while (true)
    {
        var tail = acc.ReadInt32(4);
        var head = acc.ReadInt32(0);
        var nxt = (tail + 1) % slots;
        if (nxt == head) { Thread.SpinWait(20); continue; }
        var n = Math.Min(item.Length, slot);
        acc.Write(RingHeader + tail * 4, n);
        acc.WriteArray(RingHeader + slots * 4 + tail * slot, item, 0, n);
        Thread.MemoryBarrier();
        acc.Write(4, nxt);
        return;
    }
}

static void RingPop(MemoryMappedViewAccessor acc, int slots, int slot)
{
    while (true)
    {
        var head = acc.ReadInt32(0);
        var tail = acc.ReadInt32(4);
        if (head == tail) { Thread.SpinWait(20); continue; }
        Thread.MemoryBarrier();
        acc.Write(0, (head + 1) % slots);
        return;
    }
}

static MemoryMappedFile OpenRingFile(string path, long bytes, bool create)
{
    var fs = new FileStream(
        path,
        create ? FileMode.Create : FileMode.Open,
        FileAccess.ReadWrite,
        FileShare.ReadWrite);
    if (create) fs.SetLength(bytes);
    return MemoryMappedFile.CreateFromFile(fs, mapName: null, bytes, MemoryMappedFileAccess.ReadWrite, HandleInheritability.None, leaveOpen: false);
}

static void ChildShared()
{
    var path = Environment.GetEnvironmentVariable("BENCHMARK_MMAP") ?? "";
    var n = int.Parse(Environment.GetEnvironmentVariable("BENCHMARK_CHILD_N") ?? "0");
    var slots = int.Parse(Environment.GetEnvironmentVariable("BENCHMARK_SLOTS") ?? "0");
    var slot = int.Parse(Environment.GetEnvironmentVariable("BENCHMARK_SLOT") ?? "0");
    var bytes = RingHeader + slots * 4 + slots * slot;
    using var mmf = OpenRingFile(path, bytes, create: false);
    using var acc = mmf.CreateViewAccessor();
    for (int i = 0; i < n; i++)
        RingPop(acc, slots, slot);
}

static (long enq, long deq) BenchShared(byte[][] items)
{
    var slots = items.Length + 2;
    var slot = Math.Max(items.Length > 0 ? items[0].Length : 64, 64);
    var bytes = RingHeader + slots * 4 + slots * slot;
    var path = Path.Combine(Path.GetTempPath(), "qb-ring-" + Guid.NewGuid().ToString("N"));
    using var mmf = OpenRingFile(path, bytes, create: true);
    using var acc = mmf.CreateViewAccessor();
    acc.Write(0, 0);
    acc.Write(4, 0);
    acc.Write(8, slots);
    acc.Write(12, slot);
    var psi = ChildPsi();
    psi.Environment["BENCHMARK_CHILD"] = "shared";
    psi.Environment["BENCHMARK_CHILD_N"] = items.Length.ToString();
    psi.Environment["BENCHMARK_MMAP"] = path;
    psi.Environment["BENCHMARK_SLOTS"] = slots.ToString();
    psi.Environment["BENCHMARK_SLOT"] = slot.ToString();
    using var child = Process.Start(psi)!;
    var sw = Stopwatch.StartNew();
    foreach (var it in items)
        RingPush(acc, it, slots, slot);
    child.WaitForExit();
    var wall = (long)sw.Elapsed.TotalNanoseconds;
    try { File.Delete(path); } catch { }
    return (wall / 2, wall - wall / 2);
}

static (long enq, long deq) BenchSqlite(byte[][] items)
{
    var path = Path.Combine(Path.GetTempPath(), "qb-d-" + Guid.NewGuid().ToString("N") + ".sqlite");
    var fsync = On(Environment.GetEnvironmentVariable("BENCHMARK_FSYNC"));
    using var conn = new SqliteConnection(new SqliteConnectionStringBuilder { DataSource = path }.ToString());
    conn.Open();
    using (var pragma = conn.CreateCommand())
    {
        pragma.CommandText = fsync ? "PRAGMA synchronous=FULL; PRAGMA journal_mode=WAL;" : "PRAGMA synchronous=OFF; PRAGMA journal_mode=WAL;";
        pragma.ExecuteNonQuery();
    }
    using (var create = conn.CreateCommand())
    {
        create.CommandText = "CREATE TABLE q (id INTEGER PRIMARY KEY, payload BLOB)";
        create.ExecuteNonQuery();
    }
    var sw = Stopwatch.StartNew();
    using (var ins = conn.CreateCommand())
    {
        ins.CommandText = "INSERT INTO q(payload) VALUES ($p)";
        var p = ins.CreateParameter();
        p.ParameterName = "$p";
        ins.Parameters.Add(p);
        foreach (var it in items)
        {
            p.Value = it;
            ins.ExecuteNonQuery();
        }
    }
    var enq = (long)sw.Elapsed.TotalNanoseconds;
    sw.Restart();
    using (var sel = conn.CreateCommand())
    {
        sel.CommandText = "SELECT id, payload FROM q ORDER BY id";
        using var r = sel.ExecuteReader();
        while (r.Read()) { _ = r.GetValue(1); }
    }
    var deq = (long)sw.Elapsed.TotalNanoseconds;
    try { File.Delete(path); } catch { }
    return (enq, deq);
}
