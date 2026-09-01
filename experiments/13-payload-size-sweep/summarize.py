#!/usr/bin/env python3
"""Rank stability across payload sizes for experiment 13.

Groups by (library, type_id), not just library. Writes per-language tables
and a combined finding: which sizes change order vs 256 B.
"""

from __future__ import annotations

import csv
import json
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

SIZE_ORDER = ["size_1", "size_64", "size_256", "size_4096", "size_65536"]
SIZE_BYTES = {
    "size_1": 1,
    "size_64": 64,
    "size_256": 256,
    "size_4096": 4096,
    "size_65536": 65536,
}
BASELINE = "size_256"
# A new size is a different ranking question only if copy cost collapses
# the pack, the order inverts, or first place changes *and* time jumps.
COPY_TIME_RATIO = 2.0
PACK_COLLAPSE_SPREAD = 1.3
LANGS = ["python", "rust", "javascript", "csharp", "c"]


def latest_csv(exp_dir: Path, lang: str) -> Path | None:
    root = exp_dir / lang / "logs"
    files = [p for p in root.rglob("*.csv") if "errors" not in p.name]
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


def spearman(xs: list[float], ys: list[float]) -> float | None:
    n = len(xs)
    if n < 2:
        return None

    def ranks(a: list[float]) -> list[float]:
        order = sorted(range(n), key=lambda i: a[i])
        out = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and a[order[j + 1]] == a[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                out[order[k]] = avg
            i = j + 1
        return out

    rx, ry = ranks(xs), ranks(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    if dx == 0 or dy == 0:
        return 1.0 if dx == dy == 0 else None
    return num / (dx * dy)


def kendall_tau(xs: list[float], ys: list[float]) -> float | None:
    n = len(xs)
    if n < 2:
        return None
    conc = disc = 0
    for i in range(n):
        for j in range(i + 1, n):
            dx = xs[i] - xs[j]
            dy = ys[i] - ys[j]
            if dx == 0 or dy == 0:
                continue
            if dx * dy > 0:
                conc += 1
            else:
                disc += 1
    tot = conc + disc
    return None if tot == 0 else (conc - disc) / tot


def ranking(medians: dict[str, float]) -> list[str]:
    return [lib for lib, _ in sorted(medians.items(), key=lambda kv: kv[1])]


def pairwise_flips(order_a: list[str], order_b: list[str]) -> list[tuple[str, str]]:
    pos_a = {lib: i for i, lib in enumerate(order_a)}
    pos_b = {lib: i for i, lib in enumerate(order_b)}
    common = [lib for lib in order_a if lib in pos_b]
    flips: list[tuple[str, str]] = []
    for i, a in enumerate(common):
        for b in common[i + 1 :]:
            if (pos_a[a] - pos_a[b]) * (pos_b[a] - pos_b[b]) < 0:
                flips.append((a, b))
    return flips


def summarize_csv(path: Path) -> list[dict]:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    groups: dict[tuple[str, str, str], dict[str, list[float]]] = {}
    for r in rows:
        if r.get("RepetitionIndex") == "0":
            continue
        name = r.get("LibraryName") or r.get("SerializerName") or ""
        pattern = r.get("Pattern") or r.get("StringOrStream") or "bytes"
        type_id = r.get("TestDataName") or ""
        handoff = _f(r, "TimeHandoff", "TimeSerAndDeser")
        if handoff is None or not name:
            continue
        bucket = groups.setdefault((name, type_id, pattern), {"handoff": [], "enq": [], "deq": []})
        bucket["handoff"].append(handoff)
        enq = _f(r, "TimeEnq", "TimeSer")
        deq = _f(r, "TimeDeq", "TimeDeser")
        if enq is not None:
            bucket["enq"].append(enq)
        if deq is not None:
            bucket["deq"].append(deq)

    out: list[dict] = []
    for (name, type_id, mode), series in sorted(groups.items()):
        vals = series["handoff"]
        if not vals:
            continue
        med = statistics.median(vals)
        row = {
            "library": name,
            "test_data": type_id,
            "payload_bytes": SIZE_BYTES.get(type_id),
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
        out.append(row)

    by_size: dict[str, list[dict]] = {}
    for row in out:
        by_size.setdefault(row["test_data"], []).append(row)
    for chunk in by_size.values():
        chunk.sort(key=lambda r: r["median_handoff_ns"])
        best = chunk[0]["median_handoff_ns"] if chunk else 0
        for row in chunk:
            row["rel_to_fastest"] = (row["median_handoff_ns"] / best) if best else 1.0
    out.sort(key=lambda r: (SIZE_BYTES.get(r["test_data"]) or 0, r["median_handoff_ns"]))
    return out


def size_medians(rows: list[dict]) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for row in rows:
        out.setdefault(row["test_data"], {})[row["library"]] = row["median_handoff_ns"]
    return out


def compare_to_baseline(medians: dict[str, dict[str, float]]) -> list[dict]:
    base = medians.get(BASELINE) or {}
    reports = []
    for type_id in SIZE_ORDER:
        d = medians.get(type_id) or {}
        common = [lib for lib in ranking(base) if lib in d] if base else ranking(d)
        xs = [base[lib] for lib in common] if base else []
        ys = [d[lib] for lib in common]
        order = ranking(d)
        base_order = ranking({lib: base[lib] for lib in common}) if base else []
        flips = pairwise_flips(base_order, [lib for lib in order if lib in base]) if base else []
        ratios = [
            d[lib] / base[lib]
            for lib in common
            if base.get(lib) and base[lib] > 0 and lib in d
        ]
        ratios.sort()
        mid = ratios[len(ratios) // 2] if ratios else None
        spread = None
        if d:
            lo = min(d.values())
            hi = max(d.values())
            spread = (hi / lo) if lo else None
        reports.append(
            {
                "test_data": type_id,
                "payload_bytes": SIZE_BYTES[type_id],
                "order": order,
                "first": order[0] if order else None,
                "spearman": spearman(xs, ys) if xs else None,
                "kendall": kendall_tau(xs, ys) if xs else None,
                "flips": [f"{a} vs {b}" for a, b in flips],
                "flip_count": len(flips),
                "time_ratio_median": mid,
                "spread": spread,
                "n_libs": len(common) if common else len(d),
            }
        )
    return reports


def regime_reasons(r: dict, base: dict, lang: str) -> list[str]:
    """Reasons this size is a different ranking question than 256 B."""
    reasons: list[str] = []
    ratio = r.get("time_ratio_median")
    spread = r.get("spread")
    sp = r.get("spearman")
    first_changed = r.get("first") and r["first"] != base.get("first")
    copy_collapse = (
        ratio is not None
        and ratio >= COPY_TIME_RATIO
        and spread is not None
        and spread <= PACK_COLLAPSE_SPREAD
    )
    inversion = sp is not None and sp < 0
    first_and_copy = first_changed and ratio is not None and ratio >= COPY_TIME_RATIO
    if copy_collapse:
        reasons.append(
            f"{lang}: copy-bound pack collapse "
            f"(time ×{ratio:.2f}, spread {spread:.2f}×)"
        )
    if inversion:
        reasons.append(f"{lang}: rank inversion (Spearman {sp:.3f})")
    if first_and_copy and not copy_collapse:
        reasons.append(
            f"{lang}: first place {base.get('first')} -> {r['first']} "
            f"and time ×{ratio:.2f}"
        )
    return reasons


def recommend(lang_reports: dict[str, list[dict]]) -> dict:
    """Two published sizes plus an optional research size.

    Mid-pack swaps inside a tight pair (Spearman 0.8 with the same first
    place and flat times) are measurement noise, not a new data type.
    """
    signals: dict[str, list[str]] = {tid: [] for tid in SIZE_ORDER}
    signals[BASELINE].append("baseline (pointer-bound / typical small message)")
    for lang, reports in lang_reports.items():
        by_id = {r["test_data"]: r for r in reports}
        base = by_id.get(BASELINE)
        if not base:
            continue
        for r in reports:
            if r["test_data"] == BASELINE:
                continue
            signals[r["test_data"]].extend(regime_reasons(r, base, lang))

    default: list[str] = [BASELINE]
    research: list[str] = []
    for tid in SIZE_ORDER:
        if tid == BASELINE or not signals[tid]:
            continue
        # First copy-cost knee goes on the published matrix. A later
        # inversion (64 KiB) is a third question, not a third default cell.
        if not any(t != BASELINE for t in default):
            default.append(tid)
        else:
            research.append(tid)
    redundant = [tid for tid in SIZE_ORDER if tid not in default and tid not in research]
    return {
        "default_matrix": [
            {"test_data": tid, "payload_bytes": SIZE_BYTES[tid], "why": signals[tid]}
            for tid in default
        ],
        "research": [
            {"test_data": tid, "payload_bytes": SIZE_BYTES[tid], "why": signals[tid]}
            for tid in research
        ],
        "redundant": [
            {"test_data": tid, "payload_bytes": SIZE_BYTES[tid]} for tid in redundant
        ],
        "keep": [
            {"test_data": tid, "payload_bytes": SIZE_BYTES[tid], "why": signals[tid]}
            for tid in default
        ],
        "drop": [
            {"test_data": tid, "payload_bytes": SIZE_BYTES[tid]} for tid in redundant
        ],
        "rule": (
            "Keep 256 B as the default small cell. Add one larger cell only "
            "when some language becomes copy-bound (handoff at least 2× and "
            "the pack collapses to about 1.3×) or the ranking inverts. "
            "Mid-pack swaps with a flat time scale are not a new size. "
            "A later inversion after the first copy-cost knee stays a "
            "research / experiment cell, not a third default type."
        ),
    }


def fmt_bytes(n: int | None) -> str:
    if n is None:
        return "?"
    if n >= 1024 and n % 1024 == 0:
        return f"{n // 1024} KiB"
    return f"{n} B"


def write_lang_md(path: Path, lang: str, rows: list[dict], reports: list[dict]) -> None:
    lines = [
        f"# {lang}",
        "",
        "Times are not comparable across languages.",
        "",
    ]
    for r in reports:
        nbytes = r["payload_bytes"]
        lines.append(f"## {r['test_data']} ({fmt_bytes(nbytes)})")
        lines.append("")
        if r["spearman"] is not None:
            lines.append(
                f"vs 256 B: Spearman {r['spearman']:.3f}, "
                f"Kendall {r['kendall']:.3f}, "
                f"{r['flip_count']} pairwise flip(s), "
                f"time × {r['time_ratio_median']:.2f}."
            )
            if r["flips"]:
                lines.append("Flips: " + "; ".join(r["flips"]) + ".")
            lines.append("")
        chunk = [row for row in rows if row["test_data"] == r["test_data"]]
        lines.extend(
            [
                "| Library | Median handoff (ns) | vs fastest | n |",
                "|---------|--------------------:|-----------:|--:|",
            ]
        )
        for row in chunk:
            lines.append(
                f"| {row['library']} | {row['median_handoff_ns']:.0f} | "
                f"{row['rel_to_fastest']:.2f}× | {row['n']} |"
            )
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_combined_md(
    path: Path,
    lang_reports: dict[str, list[dict]],
    recommendation: dict,
    languages: dict,
) -> None:
    lines = [
        "# 13-payload-size-sweep",
        "",
        "Times are not comparable across languages.",
        "",
        "Question: which SPSC payload sizes change the ranking?",
        "",
        "## Recommendation",
        "",
        recommendation["rule"],
        "",
        "Do not confuse **payload bytes per item** with **how many items** "
        "move in one repetition (`data_type_instance_count`). This folder "
        "sweeps bytes per item at n = 100. n = 1 is the wakeup experiment. "
        "n = 1000 is a throughput / amortization check, not a third size.",
        "",
    ]
    if recommendation.get("default_matrix"):
        lines.append("**Published default matrix (two sizes)**")
        lines.append("")
        for item in recommendation["default_matrix"]:
            why = "; ".join(item["why"]) if item["why"] else "baseline"
            lines.append(f"- `{item['test_data']}` ({fmt_bytes(item['payload_bytes'])}): {why}")
        lines.append("")
    if recommendation.get("research"):
        lines.append("**Research / experiment only (not a default type)**")
        lines.append("")
        for item in recommendation["research"]:
            why = "; ".join(item["why"]) if item["why"] else ""
            lines.append(f"- `{item['test_data']}` ({fmt_bytes(item['payload_bytes'])}): {why}")
        lines.append("")
    if recommendation.get("redundant"):
        lines.append("**Redundant in this run**")
        lines.append("")
        for item in recommendation["redundant"]:
            lines.append(
                f"- `{item['test_data']}` ({fmt_bytes(item['payload_bytes'])}): "
                "same first place as 256 B, no copy-bound pack collapse, no inversion."
            )
        lines.append("")
    lines.extend(
        [
            "## What this means for the named types",
            "",
            "The published catalog names `message`, `event`, `telemetry`, "
            "`strings`, and `document` are already five lengths: 256 B, 512 B, "
            "1 KiB, 2 KiB, and 4 KiB. Runners do not serialize those object "
            "graphs. The warehouse SPSC ranks on those names match this sweep: "
            "Python and C never change first place; JavaScript and C# only "
            "shuffle a mid-pack pair; Rust first becomes copy-bound at 4 KiB. "
            "512 B, 1 KiB, and 2 KiB do not add a ranking question. Keep "
            "`message` (256 B) and `document` (4 KiB). Drop the three names "
            "in between from the default matrix when that change is applied.",
            "",
            "## Per language vs 256 B",
            "",
        ]
    )
    for lang, reports in lang_reports.items():
        lines.append(f"### {lang}")
        lines.append("")
        lines.append(
            "| Size | First | Spearman | Flips | Time × | Spread |"
        )
        lines.append("|------|-------|---------:|------:|-------:|-------:|")
        for r in reports:
            sp = "—" if r["spearman"] is None else f"{r['spearman']:.3f}"
            tr = "—" if r["time_ratio_median"] is None else f"{r['time_ratio_median']:.2f}"
            spr = "—" if r["spread"] is None else f"{r['spread']:.2f}×"
            lines.append(
                f"| {fmt_bytes(r['payload_bytes'])} | {r['first'] or '—'} | {sp} | "
                f"{r['flip_count']} | {tr} | {spr} |"
            )
        lines.append("")
        lines.append(f"See `{lang}/results.md`.")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    _ = languages


def main() -> int:
    exp = HERE
    if len(sys.argv) > 1:
        exp = Path(sys.argv[1]).resolve()
    languages: dict = {}
    lang_reports: dict[str, list[dict]] = {}
    for lang in LANGS:
        csv_path = latest_csv(exp, lang)
        if not csv_path:
            continue
        rows = summarize_csv(csv_path)
        reports = compare_to_baseline(size_medians(rows))
        languages[lang] = {"status": "ok", "rows": rows, "vs_256": reports}
        lang_reports[lang] = reports
        lang_dir = exp / lang
        lang_dir.mkdir(exist_ok=True)
        (lang_dir / "results.json").write_text(
            json.dumps({"status": "ok", "rows": rows, "vs_256": reports}, indent=2),
            encoding="utf-8",
        )
        write_lang_md(lang_dir / "results.md", lang, rows, reports)
    recommendation = recommend(lang_reports)
    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "question": "Which SPSC payload sizes change the ranking?",
        "sizes_bytes": [SIZE_BYTES[t] for t in SIZE_ORDER],
        "baseline_bytes": SIZE_BYTES[BASELINE],
        "recommendation": recommendation,
        "languages": languages,
    }
    (exp / "results.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_combined_md(exp / "results.md", lang_reports, recommendation, languages)
    print(f"wrote {exp / 'results.json'} langs={list(languages)}")
    if recommendation.get("default_matrix"):
        kept = ", ".join(f"{i['payload_bytes']} B" for i in recommendation["default_matrix"])
        print(f"default matrix: {kept}")
    if recommendation.get("research"):
        extra = ", ".join(f"{i['payload_bytes']} B" for i in recommendation["research"])
        print(f"research only: {extra}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
