#!/usr/bin/env bash
set -uo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
source "$REPO/scripts/lib/config.sh"
LANGS="${*:-}"
if [[ -z "$LANGS" ]]; then
  LANGS="$(bench_read_config --enabled-langs)"
fi
export BENCHMARK_RUN_CONFIG="$HERE/run.yaml"
export BENCHMARK_SEED=42
export BENCHMARK_SPECIAL="cancel"
while IFS='|' read -r id runner_dir runner_script; do
  [[ -z "$id" ]] && continue
  skip=1
  for want in $LANGS; do
    [[ "$want" == "$id" ]] && skip=0
  done
  [[ "$skip" -eq 1 ]] && continue
  echo "=== 09-async-cancel $id ==="
  export LOG_DIR="$HERE/$id/logs/$id"
  mkdir -p "$LOG_DIR"
  bash "$REPO/$runner_dir/$runner_script" all-single
done < <(bench_read_config --lang-runners)
python3 "$REPO/experiments/lib/summarize_handoff.py" "$HERE"
echo "[DONE] 09-async-cancel"
