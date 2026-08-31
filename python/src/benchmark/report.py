"""CSV logging. Shared ABI with serializer-benchmark (see docs/analysis/METRICS.md)."""

from __future__ import annotations

import csv
import os
from dataclasses import dataclass


@dataclass
class BenchmarkLog:
    string_or_stream: str = ""
    test_data_name: str = ""
    repetitions: int = 0
    repetition_index: int = 0
    serializer_name: str = ""
    serializer_version: str = ""
    time_ser_ns: int = 0
    time_deser_ns: int = 0
    size_bytes: int = 0
    memory_peak_bytes: int = 0
    fidelity_score: float = 1.0
    data_type_instance_count: int = 0
    type_config_hash: str = ""
    native_kind: str = ""
    stream_mode: str = ""
    run_order: int = -1
    schedule_position: int = -1

    @property
    def time_ser_and_deser_ns(self) -> int:
        return self.time_ser_ns + self.time_deser_ns

    @property
    def op_per_sec_ser(self) -> float:
        return 1_000_000_000.0 / self.time_ser_ns if self.time_ser_ns > 0 else 0.0

    @property
    def op_per_sec_deser(self) -> float:
        return 1_000_000_000.0 / self.time_deser_ns if self.time_deser_ns > 0 else 0.0

    @property
    def op_per_sec_ser_and_deser(self) -> float:
        total = self.time_ser_and_deser_ns
        return 1_000_000_000.0 / total if total > 0 else 0.0


CSV_HEADER = [
    "Language",
    "StringOrStream",
    "TestDataName",
    "Repetitions",
    "RepetitionIndex",
    "SerializerName",
    "SerializerVersion",
    "TimeSer",
    "TimeDeser",
    "Size",
    "TimeSerAndDeser",
    "OpPerSecSer",
    "OpPerSecDeser",
    "OpPerSecSerAndDeser",
    "MemoryPeakBytes",
    "FidelityScore",
    "DataTypeInstanceCount",
    "TypeConfigHash",
    "SizeGzip",
    "SizeZstd",
    "NativeKind",
    "StreamMode",
    "RunOrder",
    "SchedulePosition",
]


class LogStorage:
    def __init__(self, log_file_name: str):
        self._log_file_name = log_file_name
        os.makedirs(os.path.dirname(log_file_name) or ".", exist_ok=True)
        self._file_handle = open(log_file_name, "w", newline="", encoding="utf-8")
        self._writer = csv.writer(self._file_handle)
        self._writer.writerow(CSV_HEADER)
        self._file_handle.flush()

    def write(self, log: BenchmarkLog, language: str = "python") -> None:
        self._writer.writerow(
            [
                language,
                log.string_or_stream,
                log.test_data_name,
                log.repetitions,
                log.repetition_index,
                log.serializer_name,
                log.serializer_version or "",
                log.time_ser_ns,
                log.time_deser_ns,
                log.size_bytes,
                log.time_ser_and_deser_ns,
                f"{log.op_per_sec_ser:.6f}",
                f"{log.op_per_sec_deser:.6f}",
                f"{log.op_per_sec_ser_and_deser:.6f}",
                log.memory_peak_bytes,
                f"{log.fidelity_score:.4f}",
                log.data_type_instance_count,
                log.type_config_hash,
                0,
                0,
                log.native_kind,
                log.stream_mode,
                log.run_order,
                log.schedule_position,
            ]
        )
        self._file_handle.flush()

    def close(self) -> None:
        self._file_handle.close()
