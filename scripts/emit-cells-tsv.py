#!/usr/bin/env python3
"""Emit TSV cells (type_id, payload_bytes, n, io_mode, hash) from a run config."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

_REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO / "analysis" / "src"))

from benchmark_analysis.run_config_v2 import resolve_run_config  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_config", type=Path)
    args = ap.parse_args()
    resolved = resolve_run_config(args.run_config)
    io_modes = (resolved.get("execution") or {}).get("io_modes") or ["bytes"]
    print("type_id\tpayload_bytes\tn\tio_mode\thash")
    for cell in resolved["cells"]:
        tc = cell.get("type_config") or {}
        payload = int(tc.get("payload_bytes") or 256)
        n = int(cell["data_type_instance_count"])
        th = cell.get("type_config_hash") or ""
        for mode in io_modes:
            print(f"{cell['type_id']}\t{payload}\t{n}\t{mode}\t{th}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
