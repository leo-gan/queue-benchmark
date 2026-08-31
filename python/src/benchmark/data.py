"""Payload factory. type_id → opaque bytes of catalog payload_bytes."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any

import yaml

_PAYLOAD_DEFAULTS = {
    "message": 256,
    "document": 4096,
    "telemetry": 1024,
    "strings": 2048,
    "event": 512,
}


def repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / "config" / "benchmark_config.yaml").is_file():
            return p
    return here.parents[3]


def load_run_config(path: str | os.PathLike[str] | None = None) -> dict[str, Any]:
    cfg_path = Path(
        path
        or os.environ.get("BENCHMARK_RUN_CONFIG")
        or (repo_root() / "config" / "library" / "default.yaml")
    )
    with cfg_path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_catalog() -> dict[str, Any]:
    path = repo_root() / "schemas" / "data_catalog_v2.yaml"
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def payload_bytes_for(type_id: str, type_config: dict[str, Any] | None = None) -> int:
    tc = type_config or {}
    if "payload_bytes" in tc:
        return int(tc["payload_bytes"])
    catalog = load_catalog()
    defaults = ((catalog.get("types") or {}).get(type_id) or {}).get("default_type_config") or {}
    if "payload_bytes" in defaults:
        return int(defaults["payload_bytes"])
    return _PAYLOAD_DEFAULTS.get(type_id, 256)


def make_payload(type_id: str, type_config: dict[str, Any] | None, seed: int) -> bytes:
    n = payload_bytes_for(type_id, type_config)
    raw = hashlib.sha256(f"{seed}:{type_id}".encode()).digest()
    return (raw * ((n // len(raw)) + 1))[:n]


def type_config_hash(type_config: dict[str, Any] | None) -> str:
    import json

    blob = json.dumps(type_config or {}, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(blob.encode()).hexdigest()[:12]


def expand_cells(run_cfg: dict[str, Any]) -> list[dict[str, Any]]:
    types = run_cfg.get("types") or []
    counts = run_cfg.get("data_type_instance_count") or [1]
    if isinstance(counts, int):
        counts = [counts]
    io_modes = ((run_cfg.get("execution") or {}).get("io_modes")) or ["bytes"]
    cells: list[dict[str, Any]] = []
    for row in types:
        if isinstance(row, str):
            type_id, tc = row, {}
        else:
            type_id, tc = row.get("type_id"), dict(row.get("type_config") or {})
        for n in counts:
            for mode in io_modes:
                cells.append(
                    {
                        "type_id": type_id,
                        "type_config": tc,
                        "data_type_instance_count": int(n),
                        "io_mode": str(mode),
                    }
                )
    return cells
