# Run config library

Named **run configs** select the measurement matrix:

- `types` (axis W): `type_id` + `type_config` (payload shape)
- `data_type_instance_count` (axis C): items moved per repetition
- `execution.io_modes`: `bytes` = **1P1C**, `4p4c` = **4P4C** (CSV leftover `stream` is 2P2C; not I/O)

Published type ids: `size_256` (256 B) · `size_4096` (4 KiB).  
Older experiment folders still use `message` / `document` (same lengths).  
Catalog: `schemas/data_catalog_v2.yaml`.

## Files

| File | Purpose |
|------|---------|
| `smoke.yaml` | CI / quick sanity (`size_256`, n=1, 1P1C) |
| `default.yaml` | Publication matrix (256 B and 4 KiB × [100, 1000], 1P1C and 4P4C) |

## Usage

```bash
./scripts/resolve_run_config.py config/library/default.yaml
./scripts/resolve_run_config.py config/library/smoke.yaml --pretty
```

Pin runs by **path + content hash** (sidecar). Do not edit published files in
place for experiments — copy to a new file.

See `docs/analysis/test_data_configuration.md`.
