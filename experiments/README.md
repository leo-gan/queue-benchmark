# Experiments

A laboratory notebook of narrow questions this benchmark can run.

**Read [PLAN.md](PLAN.md) first.**

Each experiment is one question. Edit that folder’s **`experiment.yaml`**.
Each language run is a subfolder. Combined numbers live in `results.json`.

- Experiment 1: [`01-spsc-handoff/`](01-spsc-handoff/) — SPSC handoff of a small message
- Experiment 2: [`02-payload-size/`](02-payload-size/) — same SPSC at 4 KiB
- Experiment 3: [`03-contention/`](03-contention/) — 1P4C / 4P1C / 4P4C
- Experiment 4: [`04-backpressure/`](04-backpressure/) — bounded queue, slow consumer
- Experiment 5: [`05-wakeup/`](05-wakeup/) — empty-queue wake
- Experiment 6: [`06-burst/`](06-burst/) — burst then drain
- Experiment 7: [`07-async-waiters/`](07-async-waiters/) — many async waiters
- Experiment 8: [`08-async-backpressure/`](08-async-backpressure/) — bounded async
- Experiment 9: [`09-async-cancel/`](09-async-cancel/) — cancel parked getters
- Experiment 10: [`10-process-ipc/`](10-process-ipc/) — category P
- Experiment 11: [`11-shared-memory/`](11-shared-memory/) — category S
- Experiment 12: [`12-durable-local/`](12-durable-local/) — category D

```bash
./experiments/01-spsc-handoff/run.sh python
python3 dashboard/scripts/sync-experiments.py
```
