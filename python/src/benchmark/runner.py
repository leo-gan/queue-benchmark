"""Python queue benchmark entrypoint."""

from __future__ import annotations

import asyncio
import os
import sys
import time
from pathlib import Path

from .data import expand_cells, load_run_config, make_payload, type_config_hash
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


def _run_sync(adapter: QueueAdapter, items: list[bytes]) -> tuple[int, int, float]:
    q = adapter.create()
    t0 = _now_ns()
    for item in items:
        adapter.enqueue(q, item)
    t1 = _now_ns()
    got: list[bytes] = []
    for _ in items:
        got.append(adapter.dequeue(q))
    t2 = _now_ns()
    ok = got == items
    return t1 - t0, t2 - t1, 1.0 if ok else 0.0


def _run_sync_mpmc(adapter: QueueAdapter, items: list[bytes]) -> tuple[int, int, float]:
    import threading

    q = adapter.create()
    n = len(items)
    half = max(1, n // 2)
    batches = [items[:half], items[half:]]
    got: list[bytes] = []
    lock = threading.Lock()
    remaining = n

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
            with lock:
                got.append(item)

    t0 = _now_ns()
    threads = [
        threading.Thread(target=producer, args=(batches[0],)),
        threading.Thread(target=producer, args=(batches[1],)),
        threading.Thread(target=consumer),
        threading.Thread(target=consumer),
    ]
    for th in threads:
        th.start()
    for th in threads:
        th.join()
    wall = _now_ns() - t0
    ok = sorted(got) == sorted(items)
    return wall // 2, wall - wall // 2, 1.0 if ok else 0.0


async def _run_async(adapter: QueueAdapter, items: list[bytes]) -> tuple[int, int, float]:
    q = adapter.create()
    t0 = _now_ns()
    for item in items:
        await adapter.enqueue_async(q, item)  # type: ignore[attr-defined]
    t1 = _now_ns()
    got: list[bytes] = []
    for _ in items:
        got.append(await adapter.dequeue_async(q))  # type: ignore[attr-defined]
    t2 = _now_ns()
    return t1 - t0, t2 - t1, 1.0 if got == items else 0.0


async def _run_async_mpmc(adapter: QueueAdapter, items: list[bytes]) -> tuple[int, int, float]:
    q = adapter.create()
    n = len(items)
    half = max(1, n // 2)
    got: list[bytes] = []

    async def producer(batch: list[bytes]) -> None:
        for item in batch:
            await adapter.enqueue_async(q, item)  # type: ignore[attr-defined]

    async def consumer(count: int) -> None:
        for _ in range(count):
            got.append(await adapter.dequeue_async(q))  # type: ignore[attr-defined]

    t0 = _now_ns()
    await asyncio.gather(
        producer(items[:half]),
        producer(items[half:]),
        consumer(half),
        consumer(n - half),
    )
    wall = _now_ns() - t0
    ok = sorted(got) == sorted(items)
    return wall // 2, wall - wall // 2, 1.0 if ok else 0.0


def _measure(adapter: QueueAdapter, items: list[bytes], io_mode: str) -> tuple[int, int, float]:
    mpmc = io_mode == "stream"
    if adapter.is_async:
        if mpmc and adapter.supports_mpmc:
            return asyncio.run(_run_async_mpmc(adapter, items))
        return asyncio.run(_run_async(adapter, items))
    if mpmc and adapter.supports_mpmc:
        return _run_sync_mpmc(adapter, items)
    return _run_sync(adapter, items)


def run(reps: int, queue_filter: str = "", data_filter: str = "") -> Path:
    seed = int(os.environ.get("BENCHMARK_SEED", "42"))
    ts = os.environ.get("BENCHMARK_TS") or time.strftime("%Y-%m-%d-%H%M%S")
    log_dir = _default_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    csv_path = log_dir / f"{ts}.csv"
    storage = LogStorage(str(csv_path))

    run_cfg = load_run_config()
    cells = expand_cells(run_cfg)
    queues = [q for q in ALL_QUEUES if not queue_filter or queue_filter.lower() in q.name.lower()]
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
        for adapter in queues:
            if io_mode == "stream" and not adapter.supports_mpmc:
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
                        stream_mode="native" if io_mode == "stream" else "",
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
