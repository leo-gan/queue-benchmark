"""ABI alias map: old serializer columns load as library / enqueue names."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from benchmark_analysis.abi import (
    CSV_HEADER,
    canonicalize_csv_record,
    canonicalize_stats_group,
    pick,
    pick_stats,
)


def test_csv_header_uses_library_and_enq():
    assert "LibraryName" in CSV_HEADER
    assert "LibraryVersion" in CSV_HEADER
    assert "TimeEnq" in CSV_HEADER
    assert "TimeHandoff" in CSV_HEADER
    assert "Pattern" in CSV_HEADER
    assert "SerializerName" not in CSV_HEADER
    assert "QueueName" not in CSV_HEADER


def test_pick_accepts_leftover_serializer_columns():
    row = {"SerializerName": "mutex-queue", "TimeSer": "12", "StringOrStream": "bytes"}
    assert pick(row, "LibraryName") == "mutex-queue"
    assert pick(row, "TimeEnq") == "12"
    assert pick(row, "Pattern") == "bytes"


def test_canonicalize_csv_record_old_and_new():
    old = canonicalize_csv_record(
        {
            "SerializerName": "orjson",
            "SerializerVersion": "3.9",
            "TimeSer": "100",
            "TimeDeser": "200",
            "TimeSerAndDeser": "300",
            "StringOrStream": "stream",
            "TestDataName": "message",
        },
        language="python",
    )
    assert old["LibraryName"] == "orjson"
    assert old["LibraryVersion"] == "3.9"
    assert old["TimeEnq"] == 100
    assert old["TimeDeq"] == 200
    assert old["TimeHandoff"] == 300
    assert old["Pattern"] == "stream"

    new = canonicalize_csv_record(
        {
            "LibraryName": "deque-lock",
            "TimeEnq": "10",
            "TimeDeq": "20",
            "TimeHandoff": "30",
            "Pattern": "bytes",
            "TestDataName": "message",
        },
        language="python",
    )
    assert new["LibraryName"] == "deque-lock"
    assert new["TimeEnq"] == 10


def test_stats_aliases_library_and_handoff():
    g = canonicalize_stats_group(
        {
            "serializer": "orjson",
            "serializer_version": "3.9",
            "avg_time_ser_ns": 1.0,
            "avg_time_deser_ns": 2.0,
            "avg_time_total_ns": 3.0,
            "ser_median_ns": 1.1,
            "total_p999_ns": 9.0,
        }
    )
    assert pick_stats(g, "library") == "orjson"
    assert pick_stats(g, "library_version") == "3.9"
    assert pick_stats(g, "avg_time_enq_ns") == 1.0
    assert pick_stats(g, "avg_time_deq_ns") == 2.0
    assert pick_stats(g, "avg_time_handoff_ns") == 3.0
    assert pick_stats(g, "enq_median_ns") == 1.1
    assert pick_stats(g, "handoff_p999_ns") == 9.0
