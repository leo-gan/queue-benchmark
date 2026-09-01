"""CSV parsing utilities for benchmark data."""

from __future__ import annotations

import csv
import os
from typing import Dict, List, Optional, Tuple

from .abi import canonicalize_csv_record


def parse_csv_file(filepath: str, language_hint: Optional[str] = None) -> Tuple[List[Dict], int]:
    """Parse benchmark CSV file and return (records, skipped_count).

    Emits canonical queue column names. Accepts leftover serializer-benchmark
    headers (``SerializerName``, ``TimeSer``, ``StringOrStream``, …) so
    historical logs keep loading.

    The second return value makes skipped/malformed rows auditable by callers.
    """
    records: List[Dict] = []
    skipped = 0
    if not filepath or not os.path.exists(filepath):
        return records, 0

    # Infer language from path if not provided
    if language_hint is None:
        low = filepath.replace("\\", "/").lower()
        # Longer / more specific path tokens first (cpp before c; javascript before…).
        for token, lang in (
            ("/csharp/", "csharp"),
            ("/c-sharp/", "csharp"),
            ("/python/", "python"),
            ("/rust/", "rust"),
            ("/javascript/", "javascript"),
            ("/logs/go/", "go"),
            ("/go/", "go"),
            ("/kotlin/", "kotlin"),
            ("/java/", "java"),
            ("/swift/", "swift"),
            ("/cpp/", "cpp"),
            ("/logs/c/", "c"),
        ):
            if token in low:
                language_hint = lang
                break
        if language_hint is None:
            # Segment-based fallback. Prefer cpp over bare "c" (logs/cpp must not
            # become Language=c). Exact segment match avoids "compat"/"case" false hits.
            parts = [p for p in low.split("/") if p]
            if "cpp" in parts or "c++" in parts or "cxx" in parts:
                language_hint = "cpp"
            elif "kotlin" in parts:
                language_hint = "kotlin"
            elif "java" in parts:
                language_hint = "java"
            elif "swift" in parts:
                language_hint = "swift"
            elif "c" in parts:
                language_hint = "c"
            elif low.endswith(("/c", "/c/", "/c.csv")):
                language_hint = "c"

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                lang = (row.get("Language") or language_hint or "").strip()
                records.append(canonicalize_csv_record(row, language=lang))
            except (ValueError, KeyError, TypeError) as e:
                skipped += 1
                print(f"Warning: Skipping malformed row: {row}, error: {e}")
    if skipped:
        print(f"Parser: skipped {skipped} malformed row(s) from {filepath}")
    return records, skipped

