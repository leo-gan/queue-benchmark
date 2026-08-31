# Claims and replication

CI **smoke-tests** runners. It does **not** publish numbers.

Published dashboard payloads are packed on a developer machine:

```bash
./scripts/run-all-benchmarks.sh --mode full --analyze
python3 dashboard/scripts/sync-data.py
```

Then commit `dashboard/public/data/` and deploy docs.

## What we claim

- Rankings are **within one language and one communication category**
  (thread vs async), on the payload types and patterns in the run config,
  on one machine, one session.
- Warmup index 0 is in the CSV; analysis drops it.
- Cross-language times are directional only.

## What we do not claim

- “The fastest queue.”
- Production tail latency under load.
- Broker (Redis/Kafka) performance.
