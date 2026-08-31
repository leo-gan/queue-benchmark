#!/usr/bin/env bash
# Run this experiment for one language (or all enabled).
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$HERE/../.." && pwd)"
# shellcheck source=../../scripts/lib/config.sh
source "$REPO/scripts/lib/config.sh"

LANGS="${*:-}"
if [[ -z "$LANGS" ]]; then
  LANGS="$(bench_read_config --enabled-langs)"
fi

export BENCHMARK_RUN_CONFIG="$HERE/run.yaml"
export BENCHMARK_SEED=42

while IFS='|' read -r id runner_dir runner_script; do
  [[ -z "$id" ]] && continue
  skip=1
  for want in $LANGS; do
    [[ "$want" == "$id" ]] && skip=0
  done
  [[ "$skip" -eq 1 ]] && continue
  echo "=== 01-spsc-handoff $id ==="
  export LOG_DIR="$HERE/$id/logs/$id"
  mkdir -p "$LOG_DIR"
  bash "$REPO/$runner_dir/$runner_script" all-single
done < <(bench_read_config --lang-runners)

echo "[DONE] 01-spsc-handoff"
