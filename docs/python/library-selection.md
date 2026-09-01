# Python library selection

This page is the include/exclude record for Python queues. Combined from
two candidate lists: distributed task-queue frameworks, and a mixed
in-process / broker-client / framework list.

This lab measures **local handoff** on one machine. Compare inside one
language and one communication category (T / A, plus opt-in P / S / D).
Brokers are category **N** and stay out of the published matrix. See
[Comparison rules](../analysis/COMPARISON_RULES.md) and
[Queue categories](../analysis/queue_categories.md).

## Decision

| Decision | Libraries |
|----------|-----------|
| **Already in** | `collections.deque` (`deque-lock`), `queue.Queue`, `asyncio.Queue`, `multiprocessing.Queue` |
| **Added** | `queue.SimpleQueue`, `janus` (async face only), `multiprocessing.SimpleQueue` (opt-in P) |
| **Out — not a handoff queue** | Celery, RQ, Huey, Dramatiq, Taskiq, ARQ, Procrastinate, TaskTiger, WakaQ, Taskflow, APScheduler, Pydantic Job Queue / typed job runners, StreaQ, ArdiQ, Nameko, FastStream |
| **Out — category N (localhost broker)** | pika, aio-pika, kombu, confluent-kafka, kafka-python / aiokafka, redis-py, boto3 (SQS), azure-servicebus, google-cloud-pubsub, nats-py, pyzmq |

The advice to prefer broker clients (#6–16 on the second list) for “raw
enqueue/dequeue” is a **different experiment**. A localhost Redis or
RabbitMQ row is client + serialize + loopback + server. It must never
share a chart with `deque-lock`.

## In this lab

| Log name | Category | Why |
|----------|----------|-----|
| `deque-lock` | T / locked | `collections.deque` + `Lock`. Locked baseline. Already present. |
| `queue.Queue` | T / concurrent | Threading MPMC with `maxsize`, `task_done`, condvar. Already present. |
| `queue.SimpleQueue` | T / concurrent | Same module, different implementation: C-accelerated, unbounded, no `task_done`. The usual faster stdlib alternative. **Added.** |
| `asyncio.Queue` | A | Event-loop queue. Already present. |
| `janus` | A | Third-party async face of `janus.Queue`. Compared only to other A libraries. The hybrid thread↔async path is not a category and is not timed. **Added.** |
| `spsc-ring` / `steal-deque` | T | Harness families, not from the candidate lists. Already present. |
| `multiprocessing.Queue` | P | Stdlib IPC. Already present, opt-in. |
| `multiprocessing.SimpleQueue` | P | Unbounded pipe; no `maxsize`. Opt-in. **Added.** |
| `shared-ring` / `sqlite-queue` | S / D | Opt-in families, not from the candidate lists. Already present. |

`queue.LifoQueue` and `queue.PriorityQueue` are the same module with
different order. FIFO vs LIFO vs priority is a **property**, not a
reason to rank them against FIFO queues.

## Out: task-queue frameworks

These accept a **callable** (or a job envelope), persist it, retry it,
and run a worker process. That is a scheduler, not a payload handoff.
JavaScript `p-queue` is the same kind of object and lives under Other.

| Library | Why not |
|---------|---------|
| **Celery** | Dominant distributed task framework. Broker + result backend + worker. DESIGN.md lists it out of T/A. |
| **RQ** | Redis job queue. Needs Redis; times the job runner, not a queue primitive. |
| **Huey** | Lightweight task queue (Redis/SQLite). Same job-runner semantics. SQLite-as-queue is already category D via `sqlite-queue`. |
| **Dramatiq** | Celery alternative on RabbitMQ/Redis. Framework, not a handoff API. |
| **Taskiq** | Async-first Celery/Dramatiq-style framework. Pluggable brokers. |
| **ARQ** | asyncio Redis jobs. Broker + worker. |
| **Procrastinate** | PostgreSQL job queue. Durable **remote** store, not local D. |
| **TaskTiger** | Redis task processing with reliability features. |
| **WakaQ** | Redis Celery alternative. |
| **Taskflow** | Workflow/orchestration (OpenStack). Not a queue. |
| **APScheduler** | Cron/interval scheduler. Same class as `p-queue`. |
| **Pydantic Job Queue / typed queues** | Typed job runners (SAQ, PgQueuer, and similar). Still jobs + a backend. |
| **StreaQ** | Async Redis queue. Category N. |
| **ArdiQ** | Redis-backed modern queue. Category N. |
| **Nameko** | Microservices/RPC on RabbitMQ. Not a handoff queue. |
| **FastStream** | Async wrapper over Kafka/RabbitMQ/NATS/Redis. Broker framework. |

In-memory or “eager” backends (Celery eager, Dramatiq StubBroker, Huey
memory) still time dispatch/retry/serialization, not `put`/`get`.

## Out: broker clients (category N)

These are the right objects for a **later localhost system report**.
They are not T, A, P, S, or D.

| Library | Broker | Why not now |
|---------|--------|-------------|
| **pika** | RabbitMQ (AMQP) | Local broker + framing. |
| **aio-pika** | RabbitMQ | Same, async client. |
| **kombu** | AMQP / Redis / SQS | Celery’s transport layer. Still a broker client. |
| **confluent-kafka** / **kafka-python** / **aiokafka** | Kafka | Needs a Kafka process. |
| **redis** (Lists/Streams) | Redis / Valkey | Ad-hoc queue on a server. |
| **boto3** (SQS) | AWS SQS | Cloud service, not a local primitive. |
| **azure-servicebus** | Azure Service Bus | Same. |
| **google-cloud-pubsub** | GCP Pub/Sub | Same. |
| **nats-py** | NATS | Local NATS is still category N. |
| **pyzmq** | ZeroMQ | DESIGN.md lists ZeroMQ out of T/A. |

Category N needs its own host requirements, payload serialization, and
a report labeled “localhost”. It is unpublished on purpose.

## Hybrid `janus`

`janus` exists to bridge a thread and an asyncio task on one queue.
That path is useful in production and **not a comparison category**
here (never rank T against A). The adapter uses only `async_q`, so the
row is an A library: “what does janus cost versus `asyncio.Queue` when
both faces are not in play?”
