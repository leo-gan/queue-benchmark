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
| `size_1` … `size_65536` | 1 B … 64 KiB | Experiment 13 size sweep only |

`data_type_instance_count` is **how many items** move through the queue in one
repetition (not “how many objects to serialize”). It is not a payload size.

Smoke uses `message` × 1 item. Default still uses all five named types ×
`[100, 1000]`. Experiment 13 found that only **256 B** and **4 KiB** change
SPSC ranking; 512 B / 1 KiB / 2 KiB are redundant names for nearby lengths.
The default matrix is not collapsed in this change.
