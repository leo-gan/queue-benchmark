#!/usr/bin/env bash
# SPSC payload-size sweep. Uses full repetitions so rank comparisons have
# more than a handful of trials.
set -uo pipefail
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
  echo "=== 13-payload-size-sweep $id ==="
  export LOG_DIR="$HERE/$id/logs/$id"
  mkdir -p "$LOG_DIR"
  bash "$REPO/$runner_dir/$runner_script" full
done < <(bench_read_config --lang-runners)

python3 "$HERE/summarize.py"
echo "[DONE] 13-payload-size-sweep"
