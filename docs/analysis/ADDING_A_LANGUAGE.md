# Adding a language

A language is a **closed-set id** (`python`, `rust`, `javascript`, `csharp`, `c`).
The folder name may differ (`c-sharp/` → id `csharp`).

## Required

```text
<runner_dir>/
  README.md
  scripts/run-benchmarks.sh
  src/   # or language equivalent
```

`scripts/run-benchmarks.sh` must:

1. `source "$PROJECT_ROOT/scripts/lib/config.sh"`
2. Accept `smoke|all-single|full|research|custom`
3. Use `bench_mode_reps` — never hard-code 2/10/100/500
4. Export `BENCHMARK_TS`, `BENCHMARK_SEED`, `bench_export_run_config`
5. Write `logs/<id>/YYYY-MM-DD-HHMMSS.csv` using the shared CSV ABI
6. Optionally write `.errors.csv` and let analysis write `.configs.json`

## Also update

- `config/benchmark_config.yaml` → `languages.<id>` and `paths.language_log_dirs`
- `scripts/check-host-requirements.sh` / `install-host-requirements.sh`
- `.github/workflows/benchmark-ci.yml`
- `mkdocs.yml` Languages nest and `docs/<lang>/index.md`
- dashboard `LANGUAGE_CATALOG` / `sync-data.py`
- `.grok/skills/prepare-pr/scripts/detect-changed-langs.sh`
