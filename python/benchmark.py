import sys
import os
import time
import asyncio
import queue
import multiprocessing
import janus
import json
import collections

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

def benchmark_multiprocessing_queue(data, total_bytes):
    q = multiprocessing.Queue()
    times_ns = multiprocessing.Manager().list()

    def producer(q, data):
        for item in data:
            q.put(item)

    def consumer(q, expected, times_ns):
        received = 0
        while received < expected:
            t0 = time.perf_counter_ns()
            _ = q.get()
            t1 = time.perf_counter_ns()
            times_ns.append(t1 - t0)
            received += 1

    prod_proc = multiprocessing.Process(target=producer, args=(q, data))
    cons_proc = multiprocessing.Process(target=consumer, args=(q, len(data), times_ns))

    prod_proc.start()
    cons_proc.start()

    prod_proc.join()
    cons_proc.join()

    stats = calculate_stats(list(times_ns), total_bytes)
    print_stats("multiprocessing.Queue", stats)

import redis
def benchmark_redis_py(data, total_bytes):
    try:
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
    except redis.ConnectionError:
        print("Skipping redis-py benchmark: Local Redis not running")
        return

    queue_name = 'test_queue'
    r.delete(queue_name)
    times_ns = []

    def producer():
        for item in data:
            r.rpush(queue_name, item)

    def consumer():
        received = 0
        while received < len(data):
            t0 = time.perf_counter_ns()
            _ = r.blpop(queue_name)
            t1 = time.perf_counter_ns()
            times_ns.append(t1 - t0)
            received += 1

    import threading
    prod_thread = threading.Thread(target=producer)
    cons_thread = threading.Thread(target=consumer)

    prod_thread.start()
    cons_thread.start()

    prod_thread.join()
    cons_thread.join()

    stats = calculate_stats(times_ns, total_bytes)
    print_stats("redis-py (local Redis)", stats)

import zmq
import zmq.asyncio
async def benchmark_zmq_asyncio(data, total_bytes):
    ctx = zmq.asyncio.Context()
    times_ns = []

    async def producer():
        sock = ctx.socket(zmq.PUSH)
        sock.bind("inproc://asyncio_test")
        await asyncio.sleep(0.1)
        for item in data:
            await sock.send_string(item)
        sock.close()

    async def consumer():
        sock = ctx.socket(zmq.PULL)
        sock.connect("inproc://asyncio_test")
        received = 0
        while received < len(data):
            t0 = time.perf_counter_ns()
            _ = await sock.recv_string()
            t1 = time.perf_counter_ns()
            times_ns.append(t1 - t0)
            received += 1
        sock.close()

    await asyncio.gather(consumer(), producer())
    ctx.term()
    stats = calculate_stats(times_ns, total_bytes)
    print_stats("zmq.asyncio (inproc)", stats)

import aiorwlock
async def benchmark_aiorwlock_deque(data, total_bytes):
    queue = collections.deque()
    lock = aiorwlock.RWLock()
    not_empty = asyncio.Event()
    times_ns = []

    async def producer():
        for item in data:
            async with lock.writer_lock:
                queue.append(item)
                not_empty.set()

    async def consumer():
        received = 0
        while received < len(data):
            await not_empty.wait()
            t0 = time.perf_counter_ns()
            async with lock.writer_lock:
                if queue:
                    _ = queue.popleft()
                    if not queue:
                        not_empty.clear()
            t1 = time.perf_counter_ns()
            times_ns.append(t1 - t0)
            received += 1

    await asyncio.gather(producer(), consumer())
    stats = calculate_stats(times_ns, total_bytes)
    print_stats("aiorwlock + deque", stats)


async def benchmark_aioqueue(data, total_bytes):
    q = asyncio.Queue() # aioqueue behaves exactly as asyncio.Queue for basics
    times_ns = []

    async def producer():
        for item in data:
            await q.put(item)

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
    print_stats("aioqueue", stats)

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
    benchmark_multiprocessing_queue(data, total_bytes)
    benchmark_redis_py(data, total_bytes)
    asyncio.run(benchmark_zmq_asyncio(data, total_bytes))
    asyncio.run(benchmark_aiorwlock_deque(data, total_bytes))


    print("Python benchmarks completed.")

if __name__ == "__main__":
    main()
