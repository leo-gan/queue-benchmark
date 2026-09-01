# Run modes

Modes live in `config/benchmark_config.yaml` under `modes:`. Scripts never
hard-code repetition counts.

| Mode | Reps | Matrix | Use |
|------|------|--------|-----|
| `smoke` | 2 | `config/library/smoke.yaml` (256 B, n=1, 1P1C) | CI, “does it run?” |
| `all-single` | 10 | default matrix | Quick full pass |
| `full` | 100 | default matrix | Publication |
| `research` | 500 | default matrix | High-power stats |
| `custom` | caller | caller filters | Ad-hoc |

```bash
./python/scripts/run-benchmarks.sh smoke
./scripts/run-all-benchmarks.sh --mode all-single --lang rust
./python/scripts/run-benchmarks.sh custom 50 "queue.Queue" "size_256"
```
