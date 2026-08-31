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
