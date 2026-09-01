# Run config library

Named **run configs** select the measurement matrix:

- `types` (axis W): `type_id` + `type_config` (payload shape)
- `data_type_instance_count` (axis C): items moved per repetition
- `execution.io_modes`: `bytes` = **SPSC**, `stream` = **MPMC** (legacy name; not I/O)

Published type ids: `size_256` (256 B) · `size_4096` (4 KiB).  
Older experiment folders still use `message` / `document` (same lengths).  
Catalog: `schemas/data_catalog_v2.yaml`.

## Files

| File | Purpose |
|------|---------|
| `smoke.yaml` | CI / quick sanity (`size_256`, n=1, SPSC) |
| `default.yaml` | Publication matrix (256 B and 4 KiB × [100, 1000], SPSC+MPMC) |

## Usage

```bash
./scripts/resolve_run_config.py config/library/default.yaml
./scripts/resolve_run_config.py config/library/smoke.yaml --pretty
```

Pin runs by **path + content hash** (sidecar). Do not edit published files in
place for experiments — copy to a new file.

See `docs/analysis/test_data_configuration.md`.
