"""Python queue benchmark entrypoint."""

from __future__ import annotations

import asyncio
import os
import sys
import threading
import time
from pathlib import Path

from .data import expand_cells, load_run_config, make_payload, type_config_hash
from .patterns import env_bound, env_slow_consumer_ns, env_special, env_wait_ns, parse_pattern
from .queues import ALL_QUEUES
from .queues.base import QueueAdapter
from .report import BenchmarkLog, LogStorage


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / "config" / "benchmark_config.yaml").is_file():
            return p
    return here.parents[3]


def _default_log_dir() -> Path:
    env = os.environ.get("LOG_DIR")
    if env:
        p = Path(env)
        return p if p.name == "python" or p.name.endswith("python") else p / "python"
    return _repo_root() / "logs" / "python"


def _now_ns() -> int:
    return time.perf_counter_ns()


def _split(items: list[bytes], parts: int) -> list[list[bytes]]:
    n = len(items)
    parts = max(1, parts)
    out: list[list[bytes]] = []
    start = 0
    for i in range(parts):
        end = n * (i + 1) // parts
        out.append(items[start:end])
        start = end
    return out


def _can_run(adapter: QueueAdapter, producers: int, consumers: int) -> bool:
    if adapter.supports_spsc_only and (producers, consumers) != (1, 1):
        return False
    if (producers > 1 or consumers > 1) and not adapter.supports_mpmc:
        return False
    return True


def _run_sync(
    adapter: QueueAdapter,
    items: list[bytes],
    producers: int,
    consumers: int,
    capacity: int | None,
    slow_ns: int,
) -> tuple[int, int, float]:
    cap = capacity if capacity is not None else len(items)
    q = adapter.create(capacity=cap)
    if producers == 1 and consumers == 1 and slow_ns <= 0:
        t0 = _now_ns()
        for item in items:
            adapter.enqueue(q, item)
        t1 = _now_ns()
        got: list[bytes] = []
        for _ in items:
            got.append(adapter.dequeue(q))
        t2 = _now_ns()
        return t1 - t0, t2 - t1, 1.0 if got == items else 0.0

    batches = _split(items, producers)
    got: list[bytes] = []
    lock = threading.Lock()
    remaining = len(items)

    def producer(batch: list[bytes]) -> None:
        for item in batch:
            adapter.enqueue(q, item)

    def consumer() -> None:
        nonlocal remaining
        while True:
            with lock:
                if remaining <= 0:
                    return
                remaining -= 1
            item = adapter.dequeue(q)
            if slow_ns:
                time.sleep(slow_ns / 1e9)
            with lock:
                got.append(item)

    t0 = _now_ns()
    threads = [threading.Thread(target=producer, args=(b,)) for b in batches if b]
    threads += [threading.Thread(target=consumer) for _ in range(consumers)]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    wall = _now_ns() - t0
    ok = sorted(got) == sorted(items)
    return wall // 2, wall - wall // 2, 1.0 if ok else 0.0


async def _run_async(
    adapter: QueueAdapter,
    items: list[bytes],
    producers: int,
    consumers: int,
    capacity: int | None,
    slow_ns: int,
) -> tuple[int, int, float]:
    cap = capacity if capacity is not None else len(items)
    q = adapter.create(capacity=cap)
    if producers == 1 and consumers == 1 and slow_ns <= 0:
        t0 = _now_ns()
        for item in items:
            await adapter.enqueue_async(q, item)  # type: ignore[attr-defined]
        t1 = _now_ns()
        got: list[bytes] = []
        for _ in items:
            got.append(await adapter.dequeue_async(q))  # type: ignore[attr-defined]
        t2 = _now_ns()
        return t1 - t0, t2 - t1, 1.0 if got == items else 0.0

    batches = _split(items, producers)
    got: list[bytes] = []
    lock = asyncio.Lock()
    remaining = len(items)

    async def producer(batch: list[bytes]) -> None:
        for item in batch:
            await adapter.enqueue_async(q, item)  # type: ignore[attr-defined]

    async def consumer() -> None:
        nonlocal remaining
        while True:
            async with lock:
                if remaining <= 0:
                    return
                remaining -= 1
            item = await adapter.dequeue_async(q)  # type: ignore[attr-defined]
            if slow_ns:
                await asyncio.sleep(slow_ns / 1e9)
            async with lock:
                got.append(item)

    t0 = _now_ns()
    await asyncio.gather(
        *[producer(b) for b in batches if b],
        *[consumer() for _ in range(consumers)],
    )
    wall = _now_ns() - t0
    ok = sorted(got) == sorted(items)
    return wall // 2, wall - wall // 2, 1.0 if ok else 0.0


def _run_wakeup(adapter: QueueAdapter, n: int, wait_ns: int) -> tuple[int, int, float]:
    q = adapter.create(capacity=2)
    latencies: list[int] = []
    item = b"x"

    def consumer() -> None:
        for _ in range(n):
            t_wait = _now_ns()
            adapter.dequeue(q)
            latencies.append(_now_ns() - t_wait)

    th = threading.Thread(target=consumer)
    th.start()
    time.sleep(0.002)
    t0 = _now_ns()
    for _ in range(n):
        time.sleep(wait_ns / 1e9)
        adapter.enqueue(q, item)
    th.join()
    wall = _now_ns() - t0
    mid = sorted(latencies)[len(latencies) // 2] if latencies else 0
    return mid, wall - mid, 1.0 if len(latencies) == n else 0.0


def _run_burst(adapter: QueueAdapter, items: list[bytes], capacity: int | None) -> tuple[int, int, float]:
    q = adapter.create(capacity=capacity or len(items))
    t0 = _now_ns()
    for item in items:
        adapter.enqueue(q, item)
    t1 = _now_ns()
    got = [adapter.dequeue(q) for _ in items]
    t2 = _now_ns()
    return t1 - t0, t2 - t1, 1.0 if got == items else 0.0


async def _run_cancel(adapter: QueueAdapter, waiters: int) -> tuple[int, int, float]:
    q = adapter.create(capacity=1)

    async def waiter() -> None:
        try:
            await adapter.dequeue_async(q)  # type: ignore[attr-defined]
        except asyncio.CancelledError:
            return

    tasks = [asyncio.create_task(waiter()) for _ in range(waiters)]
    await asyncio.sleep(0.001)
    t0 = _now_ns()
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)
    wall = _now_ns() - t0
    return wall, 0, 1.0


def _measure(adapter: QueueAdapter, items: list[bytes], io_mode: str) -> tuple[int, int, float]:
    producers, consumers = parse_pattern(io_mode)
    capacity = env_bound()
    slow_ns = env_slow_consumer_ns()
    special = env_special()
    if special == "wakeup":
        return _run_wakeup(adapter, max(1, len(items)), env_wait_ns())
    if special == "burst":
        return _run_burst(adapter, items, capacity)
    if special == "cancel":
        if not adapter.is_async:
            return 0, 0, 0.0
        return asyncio.run(_run_cancel(adapter, max(8, len(items))))
    if adapter.is_async:
        return asyncio.run(_run_async(adapter, items, producers, consumers, capacity, slow_ns))
    return _run_sync(adapter, items, producers, consumers, capacity, slow_ns)


def run(reps: int, queue_filter: str = "", data_filter: str = "") -> Path:
    seed = int(os.environ.get("BENCHMARK_SEED", "42"))
    ts = os.environ.get("BENCHMARK_TS") or time.strftime("%Y-%m-%d-%H%M%S")
    log_dir = _default_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    csv_path = log_dir / f"{ts}.csv"
    storage = LogStorage(str(csv_path))

    run_cfg = load_run_config()
    cells = expand_cells(run_cfg)
    include_psd = os.environ.get("BENCHMARK_INCLUDE_PSD", "").strip() in {"1", "true", "on"}
    psd_names = {
        n.strip()
        for n in os.environ.get("BENCHMARK_PSD_NAMES", "").split(",")
        if n.strip()
    }
    queues = []
    for q in ALL_QUEUES:
        if queue_filter and queue_filter.lower() not in q.name.lower():
            continue
        if getattr(q, "opt_in", False):
            if not include_psd and not queue_filter:
                continue
            if psd_names and q.name not in psd_names:
                continue
        queues.append(q)
    if data_filter:
        cells = [c for c in cells if data_filter.lower() in str(c["type_id"]).lower()]

    run_order = 0
    for cell in cells:
        payload = make_payload(cell["type_id"], cell["type_config"], seed)
        n = int(cell["data_type_instance_count"])
        items = [payload] * n
        size = len(payload) * n
        tc_hash = type_config_hash(cell["type_config"])
        io_mode = cell["io_mode"]
        producers, consumers = parse_pattern(io_mode)
        for adapter in queues:
            if not _can_run(adapter, producers, consumers):
                continue
            if env_special() == "cancel" and not adapter.is_async:
                continue
            if adapter.supports_spsc_only and (env_special() or env_slow_consumer_ns()):
                continue
            for i in range(reps):
                enq, deq, fid = _measure(adapter, items, io_mode)
                storage.write(
                    BenchmarkLog(
                        string_or_stream=io_mode,
                        test_data_name=cell["type_id"],
                        repetitions=reps,
                        repetition_index=i,
                        serializer_name=adapter.name,
                        serializer_version=adapter.version(),
                        time_ser_ns=enq,
                        time_deser_ns=deq,
                        size_bytes=size,
                        fidelity_score=fid,
                        data_type_instance_count=n,
                        type_config_hash=tc_hash,
                        native_kind=adapter.category,
                        stream_mode="native" if (producers, consumers) != (1, 1) else "",
                        run_order=run_order,
                        schedule_position=run_order,
                    )
                )
                run_order += 1
    storage.close()
    print(f"Wrote {csv_path}")
    return csv_path


def main() -> None:
    args = sys.argv[1:]
    reps = int(args[0]) if args else 10
    qf = args[1] if len(args) > 1 else ""
    df = args[2] if len(args) > 2 else ""
    run(reps, qf, df)


if __name__ == "__main__":
    main()
