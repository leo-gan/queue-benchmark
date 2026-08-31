# Experiments

A laboratory notebook of narrow questions this benchmark can run.

**Read [PLAN.md](PLAN.md) first.**

Each experiment is one question. Edit that folder’s **`experiment.yaml`**.
Each language run is a subfolder. Combined numbers live in `results.json`.

- Experiment 1: [`01-spsc-handoff/`](01-spsc-handoff/) — which queue is fastest for SPSC handoff of a small message?
- Experiment 2: [`02-payload-size/`](02-payload-size/) — does the ranking change when the payload grows?

```bash
./experiments/01-spsc-handoff/run.sh python
python3 dashboard/scripts/sync-experiments.py
```
