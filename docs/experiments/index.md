# Experiments

One question per folder under `experiments/`. Read [PLAN.md](../../experiments/PLAN.md).

| # | Question |
|---|----------|
| [01-spsc-handoff](../../experiments/01-spsc-handoff/) | Which queue is fastest for SPSC handoff of a small message? |
| [02-payload-size](../../experiments/02-payload-size/) | Does that ranking change at 4 KiB? |

```bash
./experiments/01-spsc-handoff/run.sh python
python3 dashboard/scripts/sync-experiments.py
```

Never compare times across languages.
