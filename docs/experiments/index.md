# Experiments

One question per folder under `experiments/`. Read [PLAN.md](../../experiments/PLAN.md).

| # | Question |
|---|----------|
| [01-spsc-handoff](../../experiments/01-spsc-handoff/) | 1P1C handoff of a small message |
| [02-payload-size](../../experiments/02-payload-size/) | Same 1P1C at 4 KiB |
| [03-contention](../../experiments/03-contention/) | 1P4C / 4P1C / 4P4C |
| [04-backpressure](../../experiments/04-backpressure/) | Bounded queue, slow consumer |
| [05-wakeup](../../experiments/05-wakeup/) | Empty-queue wake |
| [06-burst](../../experiments/06-burst/) | Burst then drain |
| [07-async-waiters](../../experiments/07-async-waiters/) | Many async waiters |
| [08-async-backpressure](../../experiments/08-async-backpressure/) | Bounded async |
| [09-async-cancel](../../experiments/09-async-cancel/) | Cancel parked getters |
| [10-process-ipc](../../experiments/10-process-ipc/) | Category P (Python IPC) |
| [11-shared-memory](../../experiments/11-shared-memory/) | Category S |
| [12-durable-local](../../experiments/12-durable-local/) | Category D |

```bash
./experiments/01-spsc-handoff/run.sh python
python3 dashboard/scripts/sync-experiments.py
```

Never compare times across languages.
