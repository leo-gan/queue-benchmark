# Queues 201

Costs that hide behind “put and get.”

## Memory and cache lines

A queue is a data structure plus **coordination**. Two threads sharing a
counter on the same cache line bounce that line between cores (false sharing).
A ring that puts the head and tail on different cache lines avoids that.

## Copies

If enqueue copies the payload, cost grows with `payload_bytes`. Experiment 2
asks whether ranking flips when the payload grows from 256 B to 4 KiB.

## Backpressure

A **bounded** queue makes put wait (or fail) when full. That is a feature:
the producer slows down instead of exhausting memory. Unbounded queues hide
the problem until the process dies.

## Blocking vs spinning vs yielding

- **Mutex + condvar** — sleeps; good when waits are long.
- **Spin** — burns a core; good when the other side is almost ready.
- **Async yield** — gives the event loop to someone else.

This suite times the handoff. It does not tell you which waiting style fits
your latency SLO.
