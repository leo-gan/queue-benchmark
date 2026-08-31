#!/usr/bin/env bash
# Verify host toolchains needed by language benchmark runners (does not install).
# Usage:
#   ./scripts/check-host-requirements.sh           # all enabled languages + analysis
#   ./scripts/check-host-requirements.sh csharp python
#   ./scripts/check-host-requirements.sh --all
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
# shellcheck source=lib/config.sh
source "$PROJECT_ROOT/scripts/lib/config.sh"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
FAIL=0
WARN=0

ok()   { echo -e "  ${GREEN}OK${NC}  $*"; }
miss() { echo -e "  ${RED}MISS${NC} $*"; FAIL=1; }
warn() { echo -e "  ${YELLOW}WARN${NC} $*"; WARN=$((WARN + 1)); }

need_cmd() {
  local name="$1" hint="${2:-}"
  if command -v "$name" >/dev/null 2>&1; then
    local ver
    ver="$("$name" --version 2>/dev/null | head -1 || true)"
    ok "$name${ver:+ ($ver)}"
    return 0
  fi
  miss "$name${hint:+ — $hint}"
  return 1
}

check_analysis() {
  echo "analysis (configs.json / analyze-benchmarks)"
  need_cmd python3 "Python 3.10+ recommended" || true
  need_cmd uv "https://docs.astral.sh/uv/ — also used by python benchmark runner" || true
}

check_csharp() {
  echo "csharp"
  if command -v dotnet >/dev/null 2>&1; then
    local sdks
    sdks="$(dotnet --list-sdks 2>/dev/null | tr '\n' ' ')"
    if echo "$sdks" | grep -qE '(^|[[:space:]])(8|9)\.'; then
      ok "dotnet SDK present ($sdks)"
    else
      miss "dotnet SDK 8.x (found: $sdks)"
    fi
  else
    miss "dotnet — install .NET SDK 8: ./scripts/install-host-requirements.sh csharp"
  fi
}

check_python() {
  echo "python"
  need_cmd uv "curl -LsSf https://astral.sh/uv/install.sh | sh" || true
  if command -v uv >/dev/null 2>&1; then
    ok "uv can provision Python 3.12+ via uv sync"
  fi
}

check_rust() {
  echo "rust"
  need_cmd cargo "https://rustup.rs/" || true
  need_cmd rustc || true
}

check_javascript() {
  echo "javascript"
  need_cmd node "Node.js 18+" || true
  need_cmd npm || true
}

check_c() {
  echo "c"
  need_cmd cmake "https://cmake.org/ or package manager" || true
  need_cmd cc "gcc or clang" || true
  if command -v pkg-config >/dev/null 2>&1; then
    ok "pkg-config"
  else
    warn "pkg-config not found (often needed for system libs)"
  fi
}

KNOWN=(analysis csharp python rust javascript c)

resolve_targets() {
  local args=("$@")
  if [[ ${#args[@]} -eq 0 ]]; then
    local enabled
    enabled="$(bench_read_config --enabled-langs 2>/dev/null || true)"
    TARGETS=(analysis)
    if [[ -n "$enabled" ]]; then
      # shellcheck disable=SC2206
      TARGETS+=( $enabled )
    else
      TARGETS+=(csharp python rust javascript c)
    fi
    return
  fi
  if [[ "${args[0]}" == "--all" ]]; then
    TARGETS=("${KNOWN[@]}")
    return
  fi
  TARGETS=("${args[@]}")
}

resolve_targets "$@"
echo "Checking host requirements for: ${TARGETS[*]}"
echo
for t in "${TARGETS[@]}"; do
  case "$t" in
    analysis) check_analysis ;;
    csharp|c-sharp|cs) check_csharp ;;
    python|py) check_python ;;
    rust) check_rust ;;
    javascript|js|node) check_javascript ;;
    c) check_c ;;
    *) warn "unknown target: $t" ;;
  esac
  echo
done

if [[ "$FAIL" -ne 0 ]]; then
  echo -e "${RED}Missing required tools. Run ./scripts/install-host-requirements.sh${NC}"
  exit 1
fi
if [[ "$WARN" -gt 0 ]]; then
  echo -e "${YELLOW}Completed with $WARN warning(s).${NC}"
fi
echo -e "${GREEN}Host requirements OK.${NC}"
