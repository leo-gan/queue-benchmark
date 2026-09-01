"""CSV logging. Queue ABI (see docs/analysis/METRICS.md)."""

from __future__ import annotations

import csv
import os
from dataclasses import dataclass


@dataclass
class BenchmarkLog:
    pattern: str = ""
    test_data_name: str = ""
    repetitions: int = 0
    repetition_index: int = 0
    library_name: str = ""
    library_version: str = ""
    time_enq_ns: int = 0
    time_deq_ns: int = 0
    # Fixture payload bytes for this cell (same for every library). Not a score.
    size_bytes: int = 0
    memory_peak_bytes: int = 0
    fidelity_score: float = 1.0
    data_type_instance_count: int = 0
    type_config_hash: str = ""
    native_kind: str = ""
    stream_mode: str = ""
    run_order: int = -1
    schedule_position: int = -1
    cpu_time_ns: int = 0

    @property
    def time_handoff_ns(self) -> int:
        return self.time_enq_ns + self.time_deq_ns

    @property
    def op_per_sec_enq(self) -> float:
        return 1_000_000_000.0 / self.time_enq_ns if self.time_enq_ns > 0 else 0.0

    @property
    def op_per_sec_deq(self) -> float:
        return 1_000_000_000.0 / self.time_deq_ns if self.time_deq_ns > 0 else 0.0

    @property
    def op_per_sec_handoff(self) -> float:
        total = self.time_handoff_ns
        return 1_000_000_000.0 / total if total > 0 else 0.0


CSV_HEADER = [
    "Language",
    "Pattern",
    "TestDataName",
    "Repetitions",
    "RepetitionIndex",
    "LibraryName",
    "LibraryVersion",
    "TimeEnq",
    "TimeDeq",
    "Size",
    "TimeHandoff",
    "OpPerSecEnq",
    "OpPerSecDeq",
    "OpPerSecHandoff",
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
    "CpuTimeNs",
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
                log.pattern,
                log.test_data_name,
                log.repetitions,
                log.repetition_index,
                log.library_name,
                log.library_version or "",
                log.time_enq_ns,
                log.time_deq_ns,
                log.size_bytes,
                log.time_handoff_ns,
                f"{log.op_per_sec_enq:.6f}",
                f"{log.op_per_sec_deq:.6f}",
                f"{log.op_per_sec_handoff:.6f}",
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
                log.cpu_time_ns,
            ]
        )
        self._file_handle.flush()

    def close(self) -> None:
        self._file_handle.close()
