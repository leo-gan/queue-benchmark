# Benchmark runner scripts

Scripts for running benchmark runners and analysis **locally**. GitHub Actions
may smoke-test runners, but **never** regenerates result tables or plots for
documentation — those are committed after a local `analyze-benchmarks` run.

Each run creates timestamped artifacts with the **same stem** (never overwritten):

- `YYYY-MM-DD-HHMMSS.csv` — timings
- `YYYY-MM-DD-HHMMSS.errors.csv` — runner failures (only when errors occur)
- `YYYY-MM-DD-HHMMSS.configs.json` — run config + environment sidecar

## Host toolchains (prepare once)

| Script | Role |
|--------|------|
| `check-host-requirements.sh` | Verify tools for enabled languages (or listed ids). Exit 1 if missing. |
| `install-host-requirements.sh` | Install **user-local** toolchains (dotnet → `~/.dotnet`, uv, rustup). Hints only for Node/CMake. |

```bash
./scripts/check-host-requirements.sh
./scripts/install-host-requirements.sh
./scripts/check-host-requirements.sh csharp python
```

`scripts/lib/config.sh` (sourced by every runner) prepends common user-local bins
to `PATH`.

| Language | Host toolchain | Project deps (inside runner) |
|----------|----------------|------------------------------|
| csharp | .NET SDK 8+ | `dotnet restore/build` |
| python | [uv](https://docs.astral.sh/uv/) | `uv sync` |
| rust | rustc/cargo | `cargo build --release` |
| javascript | Node.js + npm | `npm install` |
| c | cmake + C compiler | cmake build |
| analysis | python3 + uv | `uv pip install -e analysis/` |

## Scripts

### `resolve_run_config.py`

Expand a run config into resolved cells:

```bash
./scripts/resolve_run_config.py config/library/default.yaml --pretty
./scripts/resolve_run_config.py config/library/smoke.yaml --seed 42
```

### `run-all-benchmarks.sh`

```bash
./scripts/run-all-benchmarks.sh --mode smoke
./scripts/run-all-benchmarks.sh --mode full --lang python --analyze
```

### `verify-results.sh`

Sanity-check latest (or `BENCHMARK_TS`) result CSVs for enabled languages.

### `read-config.py`

Query `config/benchmark_config.yaml` from the shell (`--mode-reps`, `--enabled-langs`,
`--lang-runners`, `--run-config-for-mode`).
