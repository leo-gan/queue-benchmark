#!/usr/bin/env python3
"""Build results.json / results.md from the newest CSV under each <lang>/logs/."""

from __future__ import annotations

import csv
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent


def latest_csv(exp_dir: Path, lang: str) -> Path | None:
    root = exp_dir / lang / "logs"
    files = list(root.rglob("*.csv"))
    files = [p for p in files if "errors" not in p.name]
    if not files:
        return None
    return max(files, key=lambda p: p.stat().st_mtime)


def _f(row: dict, *keys: str) -> float | None:
    for key in keys:
        raw = row.get(key)
        if raw in (None, ""):
            continue
        try:
            return float(raw)
        except (TypeError, ValueError):
            continue
    return None


def summarize_csv(path: Path) -> list[dict]:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    groups: dict[tuple[str, str], dict[str, list[float]]] = {}
    for r in rows:
        if r.get("RepetitionIndex") == "0":
            continue
        name = r.get("LibraryName") or r.get("SerializerName") or ""
        pattern = r.get("Pattern") or r.get("StringOrStream") or "bytes"
        handoff = _f(r, "TimeHandoff", "TimeSerAndDeser")
        if handoff is None:
            continue
        bucket = groups.setdefault((name, pattern), {"handoff": [], "enq": [], "deq": [], "size": []})
        bucket["handoff"].append(handoff)
        enq = _f(r, "TimeEnq", "TimeSer")
        deq = _f(r, "TimeDeq", "TimeDeser")
        size = _f(r, "Size")
        if enq is not None:
            bucket["enq"].append(enq)
        if deq is not None:
            bucket["deq"].append(deq)
        if size is not None:
            bucket["size"].append(size)
    out = []
    for (name, mode), series in sorted(groups.items()):
        vals = series["handoff"]
        if not vals:
            continue
        med = statistics.median(vals)
        row = {
            "library": name,
            "pattern": mode,
            "io": mode,
            "n": len(vals),
            "runs": len(vals),
            "median_handoff_ns": med,
            "total_median_ns": med,
            "p50_ns": med,
            "mean_ns": statistics.fmean(vals),
        }
        if series["enq"]:
            row["enq_median_ns"] = statistics.median(series["enq"])
            row["write_median_ns"] = row["enq_median_ns"]
        if series["deq"]:
            row["deq_median_ns"] = statistics.median(series["deq"])
            row["read_median_ns"] = row["deq_median_ns"]
        if series["size"]:
            row["size_bytes"] = statistics.median(series["size"])
        out.append(row)
    out.sort(key=lambda r: r["median_handoff_ns"])
    if out:
        best = out[0]["median_handoff_ns"]
        for row in out:
            row["rel_to_fastest"] = (row["median_handoff_ns"] / best) if best else 1.0
    return out


def write_lang_md(path: Path, lang: str, rows: list[dict]) -> None:
    lines = [
        f"# {lang}",
        "",
        "| Library | Pattern | Median handoff (ns) | vs fastest | n |",
        "|---------|---------|--------------------:|-----------:|--:|",
    ]
    for r in rows:
        lines.append(
            f"| {r['library']} | {r['pattern']} | {r['median_handoff_ns']:.0f} | {r['rel_to_fastest']:.2f}× | {r['n']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: summarize_handoff.py <experiment-dir>", file=sys.stderr)
        return 2
    exp = Path(sys.argv[1]).resolve()
    langs = ["python", "rust", "javascript", "csharp", "c"]
    languages = {}
    md_parts = [f"# {exp.name}", "", "Times are not comparable across languages.", ""]
    for lang in langs:
        csv_path = latest_csv(exp, lang)
        if not csv_path:
            continue
        rows = summarize_csv(csv_path)
        languages[lang] = {"status": "ok", "rows": rows}
        lang_dir = exp / lang
        lang_dir.mkdir(exist_ok=True)
        (lang_dir / "results.json").write_text(
            json.dumps({"status": "ok", "rows": rows}, indent=2), encoding="utf-8"
        )
        write_lang_md(lang_dir / "results.md", lang, rows)
        md_parts.append(f"## {lang}")
        md_parts.append("")
        if rows:
            similar = [r["library"] for r in rows if r["rel_to_fastest"] <= 1.15]
            md_parts.append("Similar set (within 15% of fastest on this sample): " + ", ".join(similar))
            md_parts.append("")
        md_parts.append(f"See `{lang}/results.md`.")
        md_parts.append("")
    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "languages": languages,
    }
    (exp / "results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    (exp / "results.md").write_text("\n".join(md_parts), encoding="utf-8")
    print(f"wrote {exp / 'results.json'} langs={list(languages)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
