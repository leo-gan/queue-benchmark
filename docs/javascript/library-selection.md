# JavaScript library selection

Same include/exclude rule as [Python](../python/library-selection.md): this lab
measures **local handoff**. Brokers are category N. Job runners
(callable + worker + retry) are not queues.

## Decision

| Decision | Libraries |
|----------|-----------|
| **Already in** | `Array`, `fastq`, `p-queue` (scheduler / Other), `steal-deque`, opt-in P/S/D |
| **Added** | `denque`, `yocto-queue` |
| **Out — job / worker frameworks** | BullMQ, Bee-Queue, Agenda, Kue, `async.queue`, `@qkitt/queue` |
| **Out — schedulers** | `p-limit`, `@henrygd/queue`, `promise-queue` (same class as `p-queue`) |
| **Out — category N** | `amqplib`, `kafkajs`, `ioredis` / `redis`, `zeromq`, AWS SQS clients |

## In this lab

| Log name | Category | Why |
|----------|----------|-----|
| `Array` | T / locked | `push` / `shift` baseline. Already present. O(n) shift. |
| `denque` | T / locked | Production O(1) double-ended queue (Redis/Mongo clients). FIFO via `push`/`shift`. SPSC only — not worker-thread safe. **Added.** |
| `yocto-queue` | T / locked | Tiny linked-list FIFO, O(1) enqueue/dequeue. Distinct implementation from `denque`’s ring. SPSC only. **Added.** |
| `fastq` | T / concurrent | In-process work queue. Already present. |
| `p-queue` | Other / scheduler | Concurrency limiter. Not ranked as a handoff queue. |

`denque` and `yocto-queue` skip MPMC cells. Inventing MPMC with a mutex around
a single-thread deque would break [comparison rule 6](../analysis/COMPARISON_RULES.md).

## Out

BullMQ, Bee-Queue, Agenda, and Kue are Redis job runners (category J on a
broker). `async.queue` and `p-limit` limit concurrency; they do not hand a
payload from a producer to a consumer. `amqplib` / `kafkajs` / `ioredis` /
`zeromq` are category N.
