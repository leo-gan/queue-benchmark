# Test data

Payload type ids live in `schemas/data_catalog_v2.yaml`. Runners build an
**opaque byte string** of `payload_bytes` — they do not serialize object graphs.

The published axis is **payload size**, not a named object shape.

| type_id | Size | Role |
|---------|------|------|
| `size_256` | 256 B | Default small cell. Queue overhead dominates. |
| `size_4096` | 4 KiB | Default large cell. Copying the bytes starts to change ranking. |
| `message` / `document` | 256 B / 4 KiB | Same lengths; older experiments still use these names. |
| `event` / `telemetry` / `strings` | 512 B / 1 KiB / 2 KiB | Kept in the catalog; not on the default matrix. |
| `size_1` / `size_64` / `size_65536` | 1 B / 64 B / 64 KiB | Experiment 13 sweep only. |

`data_type_instance_count` is **how many items** move through the queue in one
repetition. It is not a payload size.

Smoke uses `size_256` × 1 item. Default uses `size_256` and `size_4096` ×
`[100, 1000]`.
