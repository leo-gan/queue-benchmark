#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LANG_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT="$(cd "$LANG_DIR/.." && pwd)"
# shellcheck source=../../scripts/lib/config.sh
source "$PROJECT_ROOT/scripts/lib/config.sh"

LOG_DIR="${LOG_DIR:-$PROJECT_ROOT/logs/javascript}"
mkdir -p "$LOG_DIR"

MODE="${1:-all-single}"
FILTER_SER="${2:-}"
FILTER_DATA="${3:-}"

VALID_MODES="$(bench_read_config --valid-modes 2>/dev/null || echo 'smoke all-single full research')"
case " $VALID_MODES custom " in
  *" $MODE "*) ;;
  *) echo "Usage: $0 [smoke|all-single|full|research|custom] [queueFilter] [dataFilter]"; exit 1 ;;
esac

if [[ "$MODE" == "custom" ]]; then
  REPS="${2:-10}"; FILTER_SER="${3:-}"; FILTER_DATA="${4:-}"
else
  REPS="$(bench_mode_reps "$MODE")"
  if [[ "$MODE" == "smoke" ]]; then
    FILTER_SER="${FILTER_SER:-Array}"
    FILTER_DATA="${FILTER_DATA:-message}"
  fi
fi

export BENCHMARK_TS="${BENCHMARK_TS:-$(date +%Y-%m-%d-%H%M%S)}"
export BENCHMARK_SEED="$(bench_random_seed)"
export BENCHMARK_REPO_ROOT="${BENCHMARK_REPO_ROOT:-$PROJECT_ROOT}"
bench_export_run_config "$MODE"
export LOG_DIR

CELLS_TSV="$LOG_DIR/${BENCHMARK_TS}.cells.tsv"
PYTHONPATH="$PROJECT_ROOT/analysis/src${PYTHONPATH:+:$PYTHONPATH}" \
  python3 "$PROJECT_ROOT/scripts/emit-cells-tsv.py" "$BENCHMARK_RUN_CONFIG" > "$CELLS_TSV"
export BENCHMARK_CELLS_TSV="$CELLS_TSV"

cd "$LANG_DIR"
if [[ ! -d node_modules ]]; then
  npm install
fi

ARGS=("$REPS")
[[ -n "$FILTER_SER" ]] && ARGS+=("$FILTER_SER")
[[ -n "$FILTER_DATA" ]] && ARGS+=("$FILTER_DATA")
node src/runner.js "${ARGS[@]}"

CSV="$LOG_DIR/${BENCHMARK_TS}.csv"
if [[ -f "$CSV" ]]; then
  PYTHONPATH="$PROJECT_ROOT/analysis/src${PYTHONPATH:+:$PYTHONPATH}" \
    python3 -m benchmark_analysis.environment "$CSV" >/dev/null 2>&1 || true
fi
echo "[SUCCESS] JavaScript logs in $LOG_DIR"
