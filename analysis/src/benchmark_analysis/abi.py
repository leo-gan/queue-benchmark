"""Canonical queue-benchmark CSV / stats names, plus leftover aliases.

New writes use these names. The parser still accepts leftover
serializer-benchmark columns (and a brief QueueName experiment) so
historical logs keep loading.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Tuple

# CSV header written by current runners (order is the ABI).
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

CSV_HEADER_LINE = ",".join(CSV_HEADER)

# canonical -> accepted names on disk (first is preferred)
CSV_ALIASES: Dict[str, Tuple[str, ...]] = {
    "Pattern": ("Pattern", "StringOrStream"),
    "LibraryName": ("LibraryName", "QueueName", "SerializerName"),
    "LibraryVersion": ("LibraryVersion", "QueueVersion", "SerializerVersion"),
    "TimeEnq": ("TimeEnq", "TimeSer"),
    "TimeDeq": ("TimeDeq", "TimeDeser"),
    "TimeHandoff": ("TimeHandoff", "TimeSerAndDeser"),
    "OpPerSecEnq": ("OpPerSecEnq", "OpPerSecSer"),
    "OpPerSecDeq": ("OpPerSecDeq", "OpPerSecDeser"),
    "OpPerSecHandoff": ("OpPerSecHandoff", "OpPerSecSerAndDeser"),
}

# stats JSON group fields (identity + primary averages)
STATS_ALIASES: Dict[str, Tuple[str, ...]] = {
    "library": ("library", "queue", "serializer"),
    "library_version": ("library_version", "queue_version", "serializer_version"),
    "avg_time_enq_ns": ("avg_time_enq_ns", "avg_time_ser_ns"),
    "avg_time_deq_ns": ("avg_time_deq_ns", "avg_time_deser_ns"),
    "avg_time_handoff_ns": ("avg_time_handoff_ns", "avg_time_total_ns"),
}

# leftover series prefix → canonical prefix (ser/deser/total from serializer-benchmark)
STATS_PREFIX_ALIASES: Tuple[Tuple[str, str], ...] = (
    ("enq_", "ser_"),
    ("deq_", "deser_"),
    ("handoff_", "total_"),
)

# leftover fence keys inside filter provenance blocks
FENCE_ALIASES: Dict[str, Tuple[str, ...]] = {
    "fence_enq_low_ns": ("fence_enq_low_ns", "fence_ser_low_ns"),
    "fence_enq_high_ns": ("fence_enq_high_ns", "fence_ser_high_ns"),
    "fence_deq_low_ns": ("fence_deq_low_ns", "fence_deser_low_ns"),
    "fence_deq_high_ns": ("fence_deq_high_ns", "fence_deser_high_ns"),
    "fence_handoff_low_ns": ("fence_handoff_low_ns", "fence_total_low_ns"),
    "fence_handoff_high_ns": ("fence_handoff_high_ns", "fence_total_high_ns"),
}


def first_present(row: Mapping[str, Any], names: Iterable[str]) -> Optional[Any]:
    for name in names:
        if name in row and row[name] not in (None, ""):
            return row[name]
    return None


def pick(row: Mapping[str, Any], canonical: str, default: Any = None) -> Any:
    names = CSV_ALIASES.get(canonical, (canonical,))
    val = first_present(row, names)
    return default if val is None else val


def pick_stats(row: Mapping[str, Any], canonical: str, default: Any = None) -> Any:
    names = STATS_ALIASES.get(canonical, (canonical,))
    val = first_present(row, names)
    if val is not None:
        return val
    for new_p, old_p in STATS_PREFIX_ALIASES:
        if canonical.startswith(new_p):
            old = old_p + canonical[len(new_p) :]
            val = first_present(row, (canonical, old))
            return default if val is None else val
    names = FENCE_ALIASES.get(canonical)
    if names:
        val = first_present(row, names)
        return default if val is None else val
    return default


def _as_int(value: Any, default: int = 0) -> int:
    if value in (None, ""):
        return default
    return int(float(value))


def _as_float(value: Any, default: float = 0.0) -> float:
    if value in (None, ""):
        return default
    return float(value)


def canonicalize_csv_record(row: Mapping[str, Any], language: str = "") -> Dict[str, Any]:
    """Map a raw CSV row (old or new headers) onto canonical queue keys."""
    record: Dict[str, Any] = {
        "Language": (row.get("Language") or language or "").strip(),
        "Pattern": str(pick(row, "Pattern", "") or ""),
        "TestDataName": row.get("TestDataName", "") or "",
        "Repetitions": _as_int(row.get("Repetitions", 0)),
        "RepetitionIndex": _as_int(row.get("RepetitionIndex", 0)),
        "LibraryName": str(pick(row, "LibraryName", "") or ""),
        "TimeEnq": _as_int(pick(row, "TimeEnq", 0)),
        "TimeDeq": _as_int(pick(row, "TimeDeq", 0)),
        "Size": _as_int(row.get("Size", 0)),
        "TimeHandoff": _as_int(pick(row, "TimeHandoff", 0)),
        "OpPerSecEnq": _as_float(pick(row, "OpPerSecEnq", 0)),
        "OpPerSecDeq": _as_float(pick(row, "OpPerSecDeq", 0)),
        "OpPerSecHandoff": _as_float(pick(row, "OpPerSecHandoff", 0)),
    }
    ver = pick(row, "LibraryVersion")
    if ver not in (None, ""):
        record["LibraryVersion"] = str(ver)
    optional_int = (
        "MemoryPeakBytes",
        "CpuTimeNs",
        "DataTypeInstanceCount",
        "SizeGzip",
        "SizeZstd",
        "RunOrder",
        "SchedulePosition",
    )
    for key in optional_int:
        if key in row and row[key] not in (None, ""):
            record[key] = _as_int(row[key])
    if "FidelityScore" in row and row["FidelityScore"] not in (None, ""):
        record["FidelityScore"] = _as_float(row["FidelityScore"])
    for key in ("NativeKind", "StreamMode", "TypeConfigHash"):
        if key in row and row[key] not in (None, ""):
            record[key] = str(row[key]).strip()
    return record


def canonicalize_stats_group(group: Mapping[str, Any]) -> Dict[str, Any]:
    """Copy leftover serializer-benchmark keys onto canonical queue keys.

    Old published stats JSON keeps loading; callers should prefer the new names.
    """
    out: Dict[str, Any] = dict(group)
    for canon, aliases in STATS_ALIASES.items():
        val = first_present(group, aliases)
        if val is not None and canon not in out:
            out[canon] = val
    for new_p, old_p in STATS_PREFIX_ALIASES:
        for key, val in list(group.items()):
            if not isinstance(key, str) or not key.startswith(old_p):
                continue
            new_key = new_p + key[len(old_p) :]
            if new_key not in out:
                out[new_key] = val
    filt = out.get("filter")
    if isinstance(filt, MutableMapping):
        for canon, aliases in FENCE_ALIASES.items():
            val = first_present(filt, aliases)
            if val is not None and canon not in filt:
                filt[canon] = val
    return out
