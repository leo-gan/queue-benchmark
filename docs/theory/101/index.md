# Queues 101

A **queue** is a buffer that hands work from a producer to a consumer.

| Idea | Meaning |
|------|---------|
| SPSC | One producer, one consumer |
| MPSC / MPMC | Several producers and/or consumers |
| Bounded | Put waits (or fails) when full — **backpressure** |
| Unbounded | Put always succeeds until memory is gone |
| Blocking | Get waits for an item |
| Async | Same contract, but the waiter yields the event loop |
| Locked | A mutex protects a simple structure |
| Lock-free / ring | Progress without a mutex on the happy path |

This suite measures **in-process** queues. A broker on the network is a
different experiment.

See [queue categories](../../analysis/queue_categories.md) for what we ship.
