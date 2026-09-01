# C# library selection

Same include/exclude rule as [Python](../python/library-selection.md): measure
**local handoff**. Brokers are category N. Job runners are not queues.

## Decision

| Decision | Libraries |
|----------|-----------|
| **Already in** | `Queue+lock`, `ConcurrentQueue`, `Channel`, `steal-deque`, opt-in P/S/D |
| **Added** | `BlockingCollection` |
| **Out — not a put/get queue** | TPL Dataflow `BufferBlock` / `ActionBlock` (pipeline), Disruptor-net (event framework) |
| **Out — not FIFO** | `ConcurrentStack`, `ConcurrentBag` |
| **Out — job / worker frameworks** | Hangfire, Quartz.NET, MassTransit, Rebus, NServiceBus |
| **Out — category N** | RabbitMQ.Client, StackExchange.Redis, NATS.Client, Confluent.Kafka |

`BufferBlock` was listed out of scope in DESIGN.md. It is a dataflow block, not a
handoff primitive. `Channel` already covers async. Disruptor-net is a
publish/handle framework, not `Add`/`Take`.

## In this lab

| Log name | Category | Why |
|----------|----------|-----|
| `Queue+lock` | T / locked | Locked `Queue<T>` baseline. Already present. |
| `ConcurrentQueue` | T / concurrent | Lock-free-ish MPMC, non-blocking take. Already present. |
| `BlockingCollection` | T / concurrent | Stdlib blocking + bounding wrapper (default backing: `ConcurrentQueue`). The analog of Python `queue.Queue`. **Added.** |
| `Channel` | A | Async channel. Already present. |
