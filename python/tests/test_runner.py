from benchmark.report import CSV_HEADER
from benchmark.runner import run


def test_csv_header_abi():
    assert CSV_HEADER[0] == "Language"
    assert "SerializerName" in CSV_HEADER
    assert "TimeSer" in CSV_HEADER


def test_parse_pattern():
    from benchmark.patterns import parse_pattern

    assert parse_pattern("bytes") == (1, 1)
    assert parse_pattern("stream") == (2, 2)
    assert parse_pattern("1p4c") == (1, 4)
    assert parse_pattern("4p1c") == (4, 1)
    assert parse_pattern("4p4c") == (4, 4)


def test_spsc_ring_roundtrip():
    from benchmark.queues.spsc_ring import SpscRingQueue

    q = SpscRingQueue()
    assert q.supports_mpmc is False
    ring = q.create(capacity=4)
    q.enqueue(ring, b"a")
    q.enqueue(ring, b"b")
    assert q.dequeue(ring) == b"a"
    assert q.dequeue(ring) == b"b"


def test_steal_deque_roundtrip_and_steal():
    from benchmark.queues.steal_deque import StealDequeQueue

    q = StealDequeQueue()
    assert q.category == "work-stealing"
    d = q.create()
    q.enqueue(d, b"a")
    q.enqueue(d, b"b")
    q.enqueue(d, b"c")
    # Steal-from-top is FIFO: left end.
    assert q.dequeue(d) == b"a"
    assert q.dequeue(d) == b"b"
    assert q.dequeue(d) == b"c"


def test_process_queue_cross_process():
    from benchmark.queues.process_queue import ProcessQueue, run_cross_process

    assert ProcessQueue.cross_process is True
    items = [b"a", b"b", b"c", b"d"]
    enq, deq, fid = run_cross_process(items, 1, 1, None)
    assert fid == 1.0
    assert enq > 0 and deq > 0


def test_shared_ring_cross_process():
    from benchmark.queues.shared_ring import SharedRingQueue, run_cross_process

    assert SharedRingQueue.cross_process is True
    items = [b"aa", b"bb", b"cc"]
    enq, deq, fid = run_cross_process(items, 1, 1, None)
    assert fid == 1.0
    assert enq > 0 and deq > 0
    # SPSC only — MPMC is not a shared-ring cell.
    enq0, deq0, fid0 = run_cross_process(items, 2, 2, None)
    assert (enq0, deq0, fid0) == (0, 0, 0.0)


def test_wakeup_and_burst_on_async_queue():
    from benchmark.queues.asyncio_queue import AsyncioQueue
    from benchmark.runner import _measure

    q = AsyncioQueue()
    items = [b"x", b"x", b"x", b"x"]
    import os

    os.environ["BENCHMARK_SPECIAL"] = "wakeup"
    os.environ["BENCHMARK_WAIT_NS"] = "1000"
    try:
        enq, deq, fid = _measure(q, items, "bytes")
        assert fid == 1.0
        assert enq >= 0 and deq >= 0
        os.environ["BENCHMARK_SPECIAL"] = "burst"
        enq, deq, fid = _measure(q, items, "bytes")
        assert fid == 1.0
        assert enq > 0 and deq > 0
    finally:
        os.environ.pop("BENCHMARK_SPECIAL", None)
        os.environ.pop("BENCHMARK_WAIT_NS", None)


def test_smoke_writes_rows(tmp_path, monkeypatch):
    repo = tmp_path
    # runner finds repo via config/benchmark_config.yaml; use env instead
    monkeypatch.setenv("LOG_DIR", str(tmp_path))
    monkeypatch.setenv("BENCHMARK_TS", "2026-01-01-000000")
    monkeypatch.setenv("BENCHMARK_SEED", "42")
    # Use the real repo run config / catalog via cwd of the package
    csv_path = run(2, "deque-lock", "message")
    text = csv_path.read_text(encoding="utf-8")
    assert "deque-lock" in text
    assert "message" in text
    lines = [ln for ln in text.splitlines() if ln.strip()]
    assert len(lines) >= 3  # header + 2 reps (maybe more cells)
