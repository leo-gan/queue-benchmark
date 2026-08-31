from benchmark.report import CSV_HEADER
from benchmark.runner import run


def test_csv_header_abi():
    assert CSV_HEADER[0] == "Language"
    assert "SerializerName" in CSV_HEADER
    assert "TimeSer" in CSV_HEADER


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
