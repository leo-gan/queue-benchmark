# Queues 301

How to pick an in-process queue.

| Situation | Start here |
|-----------|------------|
| One thread only | A deque or ring. Do not pay for locks you do not need. |
| One producer, one consumer | SPSC ring or a simple channel. See experiment 1. |
| Many producers | MPMC (`queue.Queue`, `ConcurrentQueue`, `crossbeam-channel`). |
| Event loop | The runtime’s own queue (`asyncio.Queue`, `Channel`, `tokio::mpsc`). |
| Need backpressure | Bounded + blocking/async wait. |
| Need a broker | Leave this lab. Redis / Kafka / ZeroMQ are a different experiment. |

**Rules of use**

1. Compare queues **inside one language**.
2. Match the pattern (SPSC vs MPMC, sync vs async) to the real program.
3. Time your payload size. A ranking on 256-byte tickets may lie about 4 KiB bodies.
4. A failed fidelity check is not a speed win.

See [architecture](../../analysis/architecture.md) and [categories](../../analysis/queue_categories.md).
