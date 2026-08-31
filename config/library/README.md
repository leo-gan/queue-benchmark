# Run config library

Named **run configs** select the measurement matrix:

- `types` (axis W): `type_id` + `type_config` (payload shape)
- `data_type_instance_count` (axis C): items moved per repetition
- `execution.io_modes`: `bytes` = **SPSC**, `stream` = **MPMC** (legacy name; not I/O)

Type ids: `message` · `document` · `telemetry` · `strings` · `event`  
(catalog: `schemas/data_catalog_v2.yaml`).

## Files

| File | Purpose |
|------|---------|
| `smoke.yaml` | CI / quick sanity (`message`, n=1, SPSC) |
| `default.yaml` | Publication matrix (all five types × [100, 1000], SPSC+MPMC) |

## Usage

```bash
./scripts/resolve_run_config.py config/library/default.yaml
./scripts/resolve_run_config.py config/library/smoke.yaml --pretty
```

Pin runs by **path + content hash** (sidecar). Do not edit published files in
place for experiments — copy to a new file.

See `docs/analysis/test_data_configuration.md`.
