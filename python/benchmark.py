import sys
import os
import time
import asyncio
import queue
import multiprocessing
import janus
import json

# Add the parent folder to path to find common module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from common.data_loader import load_data
from common.stats import calculate_stats, print_stats

async def benchmark_asyncio_queue(data, total_bytes):
    q = asyncio.Queue()
    times_ns = []

    # Producer
    async def producer():
        for item in data:
            await q.put(item)

    # Consumer
    async def consumer():
        received = 0
        while received < len(data):
            t0 = time.perf_counter_ns()
            _ = await q.get()
            t1 = time.perf_counter_ns()
            times_ns.append(t1 - t0)
            q.task_done()
            received += 1

    await asyncio.gather(producer(), consumer())
    stats = calculate_stats(times_ns, total_bytes)
    print_stats("asyncio.Queue", stats)

def benchmark_queue(data, total_bytes):
    import threading
    q = queue.Queue()
    times_ns = []

    def producer():
        for item in data:
            q.put(item)

    def consumer():
        received = 0
        while received < len(data):
            t0 = time.perf_counter_ns()
            _ = q.get()
            t1 = time.perf_counter_ns()
            times_ns.append(t1 - t0)
            q.task_done()
            received += 1

    prod_thread = threading.Thread(target=producer)
    cons_thread = threading.Thread(target=consumer)

    prod_thread.start()
    cons_thread.start()

    prod_thread.join()
    cons_thread.join()

    stats = calculate_stats(times_ns, total_bytes)
    print_stats("queue.Queue", stats)

async def benchmark_janus(data, total_bytes):
    q = janus.Queue()
    times_ns = []

    async def producer():
        for item in data:
            await q.async_q.put(item)

    async def consumer():
        received = 0
        while received < len(data):
            t0 = time.perf_counter_ns()
            _ = await q.async_q.get()
            t1 = time.perf_counter_ns()
            times_ns.append(t1 - t0)
            q.async_q.task_done()
            received += 1

    await asyncio.gather(producer(), consumer())
    stats = calculate_stats(times_ns, total_bytes)
    print_stats("janus", stats)

def main():
    data_path = sys.argv[1] if len(sys.argv) > 1 else "../datasets/test_small.jsonl"
    if not os.path.exists(data_path):
        data_path = os.path.join("datasets", "test_small.jsonl")
    print(f"Loading data from: {data_path}")
    data = load_data(data_path)
    total_bytes = sum(len(item) for item in data)
    print(f"Loaded {len(data)} records, total size: {total_bytes} bytes")

    asyncio.run(benchmark_asyncio_queue(data, total_bytes))
    benchmark_queue(data, total_bytes)
    asyncio.run(benchmark_janus(data, total_bytes))

    print("Python benchmarks completed.")

if __name__ == "__main__":
    main()
