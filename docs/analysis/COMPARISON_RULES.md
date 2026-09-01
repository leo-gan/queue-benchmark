# Comparison rules

This lab publishes **slices**, not a winner. Breaking these rules produces
a chart that looks decisive and is wrong.

## Never

1. **Never publish one “fastest queue” number.** A library that wins SPSC
   handoff of a 256-byte ticket can lose at 4 KiB, under 4 producers, or
   when the queue is bounded. Report by category × pattern × payload.

2. **Never rank across languages.** A C ring and a Python deque are not
   the same experiment. Runtimes, GCs, and clocks differ. Cross-language
   times are directional only.

3. **Never put a broker on the same plot as an in-process queue.**
   Redis, Kafka, RabbitMQ, NATS, ZeroMQ on localhost measure
   client + serialize + loopback + server. That is category **N**, a
   system bench. It does not belong next to `deque-lock`.

4. **Never rank Thread against Async.** `queue.Queue` and `asyncio.Queue`
   answer different questions. Use the dashboard **Category** filter.

5. **Never treat a scheduler as a queue.** JavaScript `p-queue` limits
   concurrency. It does not hand a payload from a producer to a consumer.
   It lives under Other, not A.

6. **Never invent MPMC.** If the library cannot run two producers and two
   consumers, skip the cell. Do not wrap an SPSC structure in a mutex and
   log it as MPMC.

## Always

- Compare **inside one language and one communication category**.
- Say **SPSC / MPMC** in prose. The CSV still says `bytes` / `stream`.
- A failed fidelity check is an error, not a speed win.
- Warmup index 0 stays in the raw CSV; analysis drops it.

## Where this is enforced

| Surface | What it does |
|---------|----------------|
| [Benchmark design](BENCHMARK_DESIGN.md) | Tests and how to read a result |
| [Queue categories](queue_categories.md) | T / A default; P / S / D opt-in; N unpublished |
| [Claims](CLAIMS_AND_REPLICATION.md) | What a published dashboard payload means |
| Dashboard Category filter | Hides the other communication model |

Experiments 3–4 (contention, backpressure) are designed, not shipped.
Do not add them by widening experiment 1’s question.
