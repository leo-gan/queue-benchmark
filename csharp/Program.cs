using System;
using System.Collections.Generic;
using System.Collections.Concurrent;
using System.Diagnostics;
using System.Threading.Channels;
using System.Threading.Tasks;
using System.Threading.Tasks.Dataflow;
using System.Threading;
using System.IO;
using Common;
using System.Text;

namespace CSharpBenchmarks
{
    class Program
    {
        static async Task Main(string[] args)
        {
            string dataPath = args.Length > 0 ? args[0] : "../datasets/test_small.jsonl";
            Console.WriteLine($"Loading data from: {dataPath}");
            var data = DataLoader.LoadData(dataPath);
            int dataCount = data.Count;
            long totalBytes = 0;
            foreach (var item in data) totalBytes += item.Length;

            Console.WriteLine($"Loaded {dataCount} records, total size: {totalBytes} bytes");

            await BenchmarkSystemQueue(data, totalBytes);
            await BenchmarkConcurrentQueue(data, totalBytes);
            await BenchmarkChannel(data, totalBytes);
            await BenchmarkBufferBlock(data, totalBytes);
            await BenchmarkBlockingCollection(data, totalBytes);

            Console.WriteLine("C# benchmarks completed.");
        }

        static async Task BenchmarkSystemQueue(List<string> data, long totalBytes)
        {
            var queue = new Queue<string>();
            var lockObj = new object();
            var times = new List<long>();
            var sw = new Stopwatch();

            var producerTask = Task.Run(() =>
            {
                foreach (var item in data)
                {
                    lock (lockObj)
                    {
                        queue.Enqueue(item);
                    }
                }
            });

            int received = 0;
            var consumerTask = Task.Run(() =>
            {
                while (received < data.Count)
                {
                    sw.Restart();
                    string? item = null;
                    bool gotItem = false;
                    lock (lockObj)
                    {
                        if (queue.Count > 0)
                        {
                            item = queue.Dequeue();
                            gotItem = true;
                        }
                    }
                    if (gotItem)
                    {
                        sw.Stop();
                        times.Add(sw.Elapsed.Ticks * 100);
                        received++;
                    }
                }
            });

            await Task.WhenAll(producerTask, consumerTask);
            var stats = Stats.Calculate(times, totalBytes);
            Stats.Print("System.Collections.Generic.Queue (locked)", stats);
        }

        static async Task BenchmarkConcurrentQueue(List<string> data, long totalBytes)
        {
            var queue = new ConcurrentQueue<string>();
            var times = new List<long>();
            var sw = new Stopwatch();

            var producerTask = Task.Run(() =>
            {
                foreach (var item in data)
                {
                    queue.Enqueue(item);
                }
            });

            int received = 0;
            var consumerTask = Task.Run(() =>
            {
                while (received < data.Count)
                {
                    sw.Restart();
                    if (queue.TryDequeue(out var item))
                    {
                        sw.Stop();
                        times.Add(sw.Elapsed.Ticks * 100);
                        received++;
                    }
                }
            });

            await Task.WhenAll(producerTask, consumerTask);
            var stats = Stats.Calculate(times, totalBytes);
            Stats.Print("System.Collections.Concurrent.ConcurrentQueue", stats);
        }

        static async Task BenchmarkChannel(List<string> data, long totalBytes)
        {
            var channel = Channel.CreateUnbounded<string>();
            var times = new List<long>();
            var sw = new Stopwatch();

            var producerTask = Task.Run(async () =>
            {
                foreach (var item in data)
                {
                    await channel.Writer.WriteAsync(item);
                }
                channel.Writer.Complete();
            });

            var consumerTask = Task.Run(async () =>
            {
                for (int i = 0; i < data.Count; i++)
                {
                    sw.Restart();
                    var item = await channel.Reader.ReadAsync();
                    sw.Stop();
                    times.Add(sw.Elapsed.Ticks * 100);
                }
            });

            await Task.WhenAll(producerTask, consumerTask);
            var stats = Stats.Calculate(times, totalBytes);
            Stats.Print("System.Threading.Channels.Channel", stats);
        }

        static async Task BenchmarkBufferBlock(List<string> data, long totalBytes)
        {
            var buffer = new BufferBlock<string>();
            var times = new List<long>();
            var sw = new Stopwatch();

            var producerTask = Task.Run(async () =>
            {
                foreach (var item in data)
                {
                    await buffer.SendAsync(item);
                }
                buffer.Complete();
            });

            var consumerTask = Task.Run(async () =>
            {
                try
                {
                    while (await buffer.OutputAvailableAsync())
                    {
                        sw.Restart();
                        var item = await buffer.ReceiveAsync();
                        sw.Stop();
                        times.Add(sw.Elapsed.Ticks * 100);
                    }
                }
                catch (InvalidOperationException) { }
            });

            await Task.WhenAll(producerTask, consumerTask);
            var stats = Stats.Calculate(times, totalBytes);
            Stats.Print("System.Threading.Tasks.Dataflow.BufferBlock", stats);
        }

        static async Task BenchmarkBlockingCollection(List<string> data, long totalBytes)
        {
            var collection = new BlockingCollection<string>();
            var times = new List<long>();
            var sw = new Stopwatch();

            var producerTask = Task.Run(() =>
            {
                foreach (var item in data)
                {
                    collection.Add(item);
                }
                collection.CompleteAdding();
            });

            var consumerTask = Task.Run(() =>
            {
                foreach (var item in collection.GetConsumingEnumerable())
                {
                    sw.Restart();
                    // item read
                    sw.Stop();
                    times.Add(sw.Elapsed.Ticks * 100);
                }
            });

            await Task.WhenAll(producerTask, consumerTask);
            var stats = Stats.Calculate(times, totalBytes);
            Stats.Print("System.Collections.Concurrent.BlockingCollection", stats);
        }
    }
}
