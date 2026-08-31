#!/usr/bin/env bash
# Install *user-local* host toolchains for language benchmark runners (no sudo).
# Project deps (uv sync, npm install, cargo fetch) stay in each language's
# run-benchmarks.sh — this script only prepares compilers/runtimes.
#
# Usage:
#   ./scripts/install-host-requirements.sh              # enabled langs + analysis tools
#   ./scripts/install-host-requirements.sh csharp python
#   ./scripts/install-host-requirements.sh --all
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
# shellcheck source=lib/config.sh
source "$PROJECT_ROOT/scripts/lib/config.sh"

echo "[INFO] Install target: user-local under \$HOME (no system packages / no Docker)"
echo

install_uv() {
  if command -v uv >/dev/null 2>&1; then
    echo "[OK] uv already present: $(command -v uv)"
    return
  fi
  echo "[INFO] Installing uv..."
  curl -LsSf https://astral.sh/uv/install.sh | sh
  bench_extend_host_path
}

install_dotnet() {
  bench_extend_host_path
  if command -v dotnet >/dev/null 2>&1 && dotnet --list-sdks 2>/dev/null | grep -qE '^8\.'; then
    echo "[OK] .NET SDK 8 present ($(dotnet --list-sdks 2>/dev/null | tr '\n' ' '))"
    return
  fi
  echo "[INFO] Installing .NET SDK 8.0 to ~/.dotnet..."
  curl -sSL https://dot.net/v1/dotnet-install.sh -o /tmp/dotnet-install.sh
  bash /tmp/dotnet-install.sh --channel 8.0 --install-dir "${HOME}/.dotnet"
  export DOTNET_ROOT="${HOME}/.dotnet"
  export PATH="${HOME}/.dotnet:${PATH}"
  echo "[OK] dotnet SDKs: $(dotnet --list-sdks 2>/dev/null | tr '\n' ' ')"
}

install_rust() {
  bench_extend_host_path
  if command -v cargo >/dev/null 2>&1; then
    echo "[OK] cargo already present: $(cargo --version)"
    return
  fi
  echo "[INFO] Installing rustup (default toolchain)..."
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
  # shellcheck disable=SC1091
  source "${HOME}/.cargo/env"
  echo "[OK] $(cargo --version)"
}

install_node_hint() {
  if command -v node >/dev/null 2>&1 && command -v npm >/dev/null 2>&1; then
    echo "[OK] node $(node --version), npm $(npm --version)"
    return
  fi
  echo "[WARN] Node.js/npm not found. Install via nvm, fnm, or your package manager:"
  echo "       https://nodejs.org/ (this script does not install system Node without sudo)"
}

install_c_hint() {
  if command -v cmake >/dev/null 2>&1 && (command -v cc >/dev/null 2>&1 || command -v gcc >/dev/null 2>&1); then
    echo "[OK] cmake $(cmake --version | head -1), cc present"
    return
  fi
  echo "[WARN] cmake / C compiler not found. On Debian/Ubuntu:"
  echo "       sudo apt-get install -y cmake build-essential"
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
echo "Installing host requirements for: ${TARGETS[*]}"
echo
for t in "${TARGETS[@]}"; do
  case "$t" in
    analysis|python|py) install_uv ;;
    csharp|c-sharp|cs) install_dotnet ;;
    rust) install_rust ;;
    javascript|js|node) install_node_hint ;;
    c) install_c_hint ;;
    *) echo "[WARN] unknown target: $t" ;;
  esac
done

echo
echo "[DONE] Re-run ./scripts/check-host-requirements.sh to verify."
