# Test data

Payload type ids live in `schemas/data_catalog_v2.yaml`. Runners build an
**opaque byte string** of `payload_bytes` — they do not serialize object graphs.

| type_id | Default size | Role |
|---------|--------------|------|
| `message` | 256 B | Small typical message |
| `event` | 512 B | Envelope |
| `telemetry` | 1 KiB | Numeric bulk |
| `strings` | 2 KiB | Text pressure |
| `document` | 4 KiB | Larger payload |

`data_type_instance_count` is **how many items** move through the queue in one
repetition (not “how many objects to serialize”).

Smoke uses `message` × 1 item. Default uses all five types × `[100, 1000]`.
